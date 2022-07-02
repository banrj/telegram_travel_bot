import requests
from config_data import config
from requests.exceptions import InvalidURL
from loguru import logger


@logger.catch
def request_to_api(url, querystring) -> str:
    """
    Базовый запрос в RapidAPI Hotels
    с помощью него остальные функции получают доступ к базе данных HotelsAPI
    :arg url: ссылка для запроса.
    :arg querystring: параметры запроса подробнее на самом сайте Rapid https://rapidapi.com/apidojo/api/hotels4/
    """
    logger.add('debug_main_api.log', level='DEBUG', format="{time} {level} {message}", rotation="45 KB",
               compression="zip")
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": config.RAPID_API_KEY
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        if response.status_code == requests.codes.ok:
            return response.text

    except [InvalidURL, TimeoutError, TypeError, UnicodeEncodeError] as err:
        logger.exception(err)
        return ''


