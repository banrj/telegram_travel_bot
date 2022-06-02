import requests
from config_data import config


def request_to_api(url, querystring):
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": config.RAPID_API_KEY
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response.text

    except Exception as err:
        print(err)
