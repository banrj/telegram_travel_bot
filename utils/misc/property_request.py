from typing import Dict, List, Union
from utils.API import request_to_api
import datetime
import json
import re


def found_hotels(querystring: Dict) -> Union[None, List[dict]]:
    """
    Функция получает параметры для поиска отелей.
    :param querystring: в параметры входит id города, кол-во отелей, даты заезда и отъезда, фильтр для поиска отелей,
    локализация и валюта(подробнее https://rapidapi.com/apidojo/api/hotels4/)
    :return: возвращает список отелей с их параметрами цены за ночь, расстояния до центра, названия отеля, адрес и
    сколько юзеру обойдется полное проживание в этом отеле, посчитав кол-во дней
    """
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = querystring
    data_out = querystring['checkOut']
    data_in = querystring['checkIn']

    result = str(request_to_api(url=url, querystring=querystring))

    pattern = '(?<=,)"results":.+?(?=,"pagination")'
    find = re.search(pattern, result)
    if not find:
        return
    days = (datetime.datetime.strptime(data_out, '%Y-%m-%d') -
            datetime.datetime.strptime(data_in, '%Y-%m-%d')).days
    find = json.loads(f"{{{find[0]}}}")
    hotels = list()

    for hotel in find['results']:
        url = 'www.hotels.com/ho{}'.format(hotel['id'])

        value = hotel['ratePlan']['price']['current']
        try:
            value = int(value[1:])
        except ValueError:
            value = value[1:]
            value = re.sub(',', '', value)
            value = int(value)
        total_price = str(days * value) + '$ за {} суток'.format(days)

        hotels.append({'hotel_name': hotel['name'],
                       'hotel_id': hotel['id'],
                       'address': hotel.get('address', {}).get('streetAddress', 'уточняйте на сайте отеля'),
                       'center_distance': hotel['landmarks'][0]['distance'],
                       'price': hotel['ratePlan']['price']['current'],
                       'total_price': total_price, 'url': url})

    return hotels


def beast_hotels(querystring: Dict, start_limit: str, end_limit: str) -> Union[None, List[dict]]:
    """
    Функция берет данные от функции found_hotels, но добавляя минимальную и максимальную цену, плюс отели теперь
    выстраиваются по расстоянию до центра, после этого мы с помощью двух аргументов находим нужные нам отели, по
    параметрам мин/макс дистанции от центра.
    :param querystring: параметры отеля как в функции found_hotels, плюс мин/макс цена.
    :param start_limit: минимальное расстояние.
    :param end_limit: максимальное расстояние.
    :return: список отелей(или None если нет совпадения), у каждого отеля есть свои параметры такие, же как found_hotels
    """
    count_limit = int(querystring["pageSize"])
    querystring["pageSize"] = 25
    raw_result = found_hotels(querystring=querystring)
    if not raw_result:
        return
    start_limit = int(start_limit)
    end_limit = int(end_limit)

    hotels = list()
    count = 0
    for hotel in raw_result:
        if count == count_limit:
            break
        hotels_variant = float(hotel['center_distance'][:-3].replace(',', '.'))
        if start_limit >= hotels_variant <= end_limit:
            hotels.append(hotel)
            count += 1

    return hotels
