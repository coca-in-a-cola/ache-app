from tokenize import String
import requests
from xml.dom.minidom import parseString
from flask import current_app
from api.model.forms import FormTask
from datetime import datetime, timedelta
import textwrap


def get_user_by_card_code(code):
    user_info = get_user_by_card_code_1C(code)
    if (user_info):
        return user_info

    return None


def get_user_by_card_code_1C(code) -> dict:
    response = requests.post(
        current_app.config['APP_1C_USER_URI'],
        auth=(current_app.config['LOGIN_1C'], current_app.config['PASSWORD_1C']),
        data=f"""
        <x:Envelope
            xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:cwe="http://1CWebApp/">
            <x:Header/>
            <x:Body>
                <cwe:ПочучитьСотрудникаПоКоду>
                    <cwe:КодКарты>{code}</cwe:КодКарты>
                </cwe:ПочучитьСотрудникаПоКоду>
            </x:Body>
        </x:Envelope>
        """.encode('UTF-8'),
        headers={'Content-Type': 'application/xml'}
    )
    xml_body = response.text

    parse_fields = {
        'fullname': ('<m:ФИО>', '</m:ФИО>'),
        'personnel_number': ('<m:ТабельныйНомер>', '</m:ТабельныйНомер>'),
        'subdivision': ('<m:Подразделение>', '</m:Подразделение>'),
        'position': ('<m:Должность>', '</m:Должность>'),
        'phone_number': ('<m:НомерТелефона>', '</m:НомерТелефона>'),
        'date_of_birth': ('<m:ДатаРождения>', '</m:ДатаРождения>'),
        'address': ('<m:АдресПрописки>', '</m:АдресПрописки>')
    }

    parsed = {
        'card_code': code,
    }

    for key in parse_fields:
        start, end = parse_fields[key]
        i = xml_body.find(start)
        j = xml_body.find(end)
        if (i != -1 and j != -1):
            parsed[key] = xml_body[i + len(start):j].strip()
    
    return parsed if len(parsed) > 1 else None


def dump_form_data(formTask: FormTask, formData: dict):
    dump = dict()
    for formField in formTask.fields:
        if (formField.name in formData):
            dump[formField.label] = formData[formField.name]
    
    return ' | '.join([f'{key}: {value}' for key, value in dump.items()])


def send_form_task(user_info, formTask: FormTask, taskNumber, formData: dict):
    data=textwrap.dedent(f"""
        <x:Envelope
        xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:dm="http://www.1c.ru/dm"
        xmlns:xs="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <x:Header/>
        <x:Body>
            <dm:execute>
                <dm:request  xsi:type="dm:DMLaunchBusinessProcessRequest">
                    <dm:dataBaseID>556d22e5-8959-4a9f-b908-147a1e751adc</dm:dataBaseID>
                    <dm:businessProcess xsi:type="dm:DMBusinessProcessPerformance">
                        <dm:name>{
                            current_app.config['APP_1C_SERVICE_EXECUTE_NAME'](
                                number = taskNumber,
                                name = formTask.title,
                                subdivision = user_info['subdivision']
                            )
                        }</dm:name>
                        <dm:objectID>
                <dm:id/>
                <dm:type>DMBusinessProcessPerformance</dm:type>
            </dm:objectID>
            <dm:author>
                <dm:name>{current_app.config['APP_1C_SERVICE_AUTHOR_NAME']}</dm:name>
                <dm:objectID>
                <dm:id>{current_app.config['APP_1C_SERVICE_AUTHOR_UUID']}</dm:id>
                <dm:type>DMUser</dm:type>
                </dm:objectID>
            </dm:author>
            <dm:importance>
                <dm:name>Обычная важность</dm:name>
                <dm:objectID>
                <dm:id>Обычная</dm:id>
                <dm:type>DMBusinessProcessTaskImportance</dm:type>
                </dm:objectID>
            </dm:importance>
            <dm:beginDate>{datetime.utcnow().isoformat()}</dm:beginDate>
            <dm:started>false</dm:started>
            <dm:completed>false</dm:completed>
            <dm:description>
                Номер заявки: {taskNumber}
                Тип: {formTask.title}
                ФИО: {user_info['fullname']}
                Дата Рождения: {datetime.fromisoformat(user_info['date_of_birth']).strftime("%d.%m.%Y")}
                Табельный номер: {user_info['personnel_number']}
                Подразделение: {user_info['subdivision']}
                Должность: {user_info['position']}
                Номер телефона: {user_info['phone_number']}
                Адрес по прописке: {user_info['address']}
                
                {"Дополнительня информация с формы:" if dump_form_data(formTask, formData) else ""}
                {dump_form_data(formTask, formData)}

            </dm:description>
            <dm:dueDate>{(datetime.utcnow() + timedelta(hours=formTask.completionTimeInHours)).isoformat()}</dm:dueDate>
            <dm:state>
                <dm:name>Активен</dm:name>
                <dm:objectID>
                <dm:id>Активен</dm:id>
                <dm:type>DMBusinessProcessState</dm:type>
                </dm:objectID>
            </dm:state>
            <dm:businessProcessTemplate xsi:type="dm:DMBusinessProcessPerformanceTemplate">
                <dm:name/>
                <dm:objectID>
                <dm:id>{current_app.config['APP_1C_SERVICE_BUSINESS_PROCESS_TEMPLATE_ID']}</dm:id>
                <dm:type>DMBusinessProcessPerformanceTemplate</dm:type>
                </dm:objectID>
            </dm:businessProcessTemplate>
            {
                " ".join([
                    (f'''
                    <dm:performers>
                    <dm:personalDueDate>{(datetime.utcnow() + timedelta(hours=performer.completionTimeInHours)).isoformat()}</dm:personalDueDate>
                    <dm:personalDescription/>
                    <dm:personalTaskName/>
                    <dm:responsible>{performer.responsible}</dm:responsible>
                    <dm:performanceOrder>
                    <dm:name>Вместе с предыдущим</dm:name>
                    <dm:objectID>
                        <dm:id>ВместеСПредыдущим</dm:id>
                        <dm:type>DMTaskExecutionOrder</dm:type>
                    </dm:objectID>
                    </dm:performanceOrder>
                    <dm:user>
                    <dm:name>{performer.fullname}</dm:name>
                    <dm:objectID>
                        <dm:id>{performer.uuid_1c}</dm:id>
                        <dm:type>DMUser</dm:type>
                    </dm:objectID>
                    </dm:user>
                    </dm:performers>
                    ''').replace(chr(10), " ")
                for performer in formTask.performers
                ])
            }
            <dm:performanceType>

            <dm:name>Всем сразу</dm:name>
                <dm:objectID>
                <dm:id>Параллельно</dm:id>
                <dm:type>DMApprovalType</dm:type>
                </dm:objectID>
            </dm:performanceType>
            </dm:businessProcess>
        </dm:request>
        </dm:execute>
        </x:Body>
    </x:Envelope>
    """)

    xml = parseString(data)
    xml_pretty_str = xml.toprettyxml()
    
    if not (current_app.config['PRODUCTION']):
        output_log = open('request.xml', 'w')
        output_log.write(xml_pretty_str)
        output_log.close()

    response = requests.post(
        current_app.config['APP_1C_SERVICE_URI'],
        auth=(current_app.config['LOGIN_1C'], current_app.config['PASSWORD_1C']),
        data=xml_pretty_str.encode('UTF-8'),
        headers={'Content-Type': 'application/xml'}
    )
    xml_body = response.text

    if not (current_app.config['PRODUCTION']):
        response_log = open('response.xml', 'w')
        response_log.write(xml_body)
        response_log.close()

    if (response.status_code == 200):
        return
    else:
        raise Exception(f'{response.status_code}')