import json
import re
from utils.API import request_to_api
from typing import List, Union


def found_cities(city_name: str) -> Union[None, List[dict]]:

    """
    Функция находит совпадения городов, по названию, которое ввел пользователь.
    :param city_name: имя города для поиска совпадений.
    :return: список городов(или None если совпадений нет), у каждого города есть параметры
    подробнее в документации https://rapidapi.com/apidojo/api/hotels4/
    """

    querystring = {"query": city_name, "locale": "ru_RU", "currency": "USD"}
    result = request_to_api(url="https://hotels4.p.rapidapi.com/locations/v2/search", querystring=querystring)
    zero_cities = re.search(r'"moresuggestions":(\d+?),', result)
    if zero_cities.group(1) == '0':
        return
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, result)
    if find:
        suggestions = json.loads(f"{{{find[0]}}}")
        cities = list()
        for city_param in suggestions['entities']:
            clear_city_param = re.sub(r'<.+?>', '', city_param['caption'])
            cities.append({'city_name': clear_city_param, 'destination_id': city_param['destinationId']})
        return cities

