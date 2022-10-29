import React, { useRef, useState } from 'react';
import Keyboard from 'react-simple-keyboard';
import 'react-simple-keyboard/build/css/index.css';
import '../../assets/css/react-simple-keyboard-custom.css'
import {Button} from '../UI/Button'
import PropTypes from 'prop-types'

export const ConfirmNumber = ({displayPhoneNumber = "+70000000000", maxLength = 5, timeout = 99, onSubmit, onCancel, onRetry}) => {
    const [input, setInput] = useState("");
    const keyboard = useRef();

    const format = (value) => {
        const pattern = value[0] == "+" ? "## (###) ### ##-##" : "# (###) ### ##-##"
        var i = 0,
            v = value.toString();
        return pattern.replace(/#/g, _ => v[i++]);
    }
    
    const onChange = (input) => {
        setInput(input);

        if (input.length >= maxLength) {
            setTimeout(() => {
                onSubmit?.(input)
                setInput("");
                keyboard.current.setInput("");
            }, 200)
        }
    }
    
    const onKeyPress = (button) => {
        console.log("Button pressed", button);
    }
    
    const onChangeInput = event => {
        const input = event.target.value;
        setInput(input);
        keyboard.current.setInput(input);    

        if (input.length >= maxLength) {
            setTimeout(() => {
                onSubmit?.(input)
                setInput("");
                keyboard.current.setInput("");
            }, 1000)
        }
    };

    return (
        <>
        <div className="container mx-auto text-center relative max-w-5xl">
        <div class="mx-auto">
        
        <form className="bg-white mt-4 left-0 right-0 shadow-md rounded px-8 py-4 mb-4">
            <h1 className="text-5xl pt-12 mx-auto text-blue-darker font-black">
                Введите код подтверждения
            </h1>
            <p className="text-2xl pt-2 max-w-4xl mx-auto text-gray-500">
                Код подтверждения отправлен на номер {format(displayPhoneNumber)}
                <br/>
                Введите его в поле ниже
            </p>
            <div className="mb-8 mt-2">

            <input
            value={input}
            name="confirm-number"
            className="border-solid border-4 border-gray-200 shadow appearance-none rounded w-72 py-2 px-3
            text-gray-500 text-center text-4xl font-black leading-tight tracking-widest focus:outline-none focus:shadow-outline"
            id="username" type="text"
            onChange={onChangeInput}
            />

            </div>
        </form>
        
        </div>
        </div>

        <div className="flex justify-between w-full max-w-5xl mx-auto">
            <Button className="w-80 bg-red" onClick={onCancel} timeout={timeout}>ВЫХОД</Button>
            <Button className="w-80 bg-blue-darker" onClick={onRetry}>ЗАПРОСИТЬ КОД ЕЩЁ РАЗ</Button>
        </div>
        
        <Keyboard
        
        keyboardRef={r => (keyboard.current = r)}
        layout={{
            default:
                ['7 8 9', '4 5 6', '1 2 3', ' 0 {bksp}']
            }}
        onChange={onChange}
        onKeyPress={onKeyPress}

        buttonTheme={[
            {
              class: "hg-icon-bksp",
              buttons: "{bksp}"
            }
          ]}


        display={{
            '{bksp}': '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0z" fill="none"/><path d="M21 11H6.83l3.58-3.59L9 6l-6 6 6 6 1.41-1.41L6.83 13H21z"/></svg>',
            }}
    
        />

        </>
    );
}

ConfirmNumber.propTypes = {

    /**
     *  Время до отмены ввода, в секундах
     */
    timeout: PropTypes.number,

    /**
     *  Длина номера подтверждения
     *  Если введено maxLength символов, форма автоматически отправляется
     */
    maxLength: PropTypes.number,

    /**
     *  Действие при отправки формы
     */
    onSubmit: PropTypes.func,

    /**
     *  Действие при повтовром запросе кода
     */
    onRetry: PropTypes.func,

    /**
     *  Действие при отмене ввода пользователем
     */
    onCancel: PropTypes.func,
}

ConfirmNumber.defaultProps = {

}