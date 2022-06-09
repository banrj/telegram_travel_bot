from typing import Dict, List, Optional
from utils.API import request_to_api
import datetime
import json
import re


def found_hotels(querystring: Dict) -> Optional[List[dict]]:
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


def beast_hotels(querystring: Dict, start_limit: str, end_limit: str) -> Optional[List[dict]]:
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
        if start_limit >= hotel['center_distance'] <= end_limit:
            hotels.append(hotel)
            count += 1

    return hotels
