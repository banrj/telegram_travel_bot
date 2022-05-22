import requests
import json
import re


def request_to_api(url, query):
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "47e4617550msh1e4d6c64aab650dp195b0djsnc84e78634d98"
    }
    querystring = {"query": query, "locale": "en_US", "currency": "USD"}
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            results = json.loads(response.text)
            return response.text

    except Exception as err:
        print(err)


result = request_to_api(url="https://hotels4.p.rapidapi.com/locations/v2/search", query='london')

pattern = r'(?<="CITY_GROUP",).+?[\]]'
find = re.search(pattern, result)
if find:
    suggestions = json.loads(f"{{{find[0]}}}")
    for i in suggestions['entities']:
        print(i)

