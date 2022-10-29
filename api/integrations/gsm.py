from flask import current_app
import urllib.parse
import requests


def send(phone, message):
    response = requests.get(current_app.config["GSM_CONNECT_STRING"]
        + f"&phonenumber={urllib.parse.quote(phone)}&message={urllib.parse.quote(message)}",
        proxies=dict(http=current_app.config['PROXY_SERVER']))
    
    if (response.ok):
        return response
    else:
        raise(Exception(f"GSM failed with response: {response.status} - {response.content}"))