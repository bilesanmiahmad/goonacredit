import requests


def send_sms(url, key, sender_id, number, message):
    querystring = {
        "api_key": key,
        "phone_numbers": number,
        "sender_id": sender_id,
        "message": message
    }
    response = requests.request("POST", url, data=querystring)
    print(response.text)
