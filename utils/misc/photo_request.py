from utils.API import request_to_api
import re
from typing import List
from telebot.types import InputMediaPhoto


def take_photo(photo_id: str, quantity: str) -> List[InputMediaPhoto]:
    """
    Функция получает фотографии отелей, добавляет размеры и возвращает их объектами InputMediaPhoto.
    :param photo_id: айди отеля, для которого нужны фотографии.
    :param quantity: кол-во фотографий.
    :return: список фотографий, которые получили свойства объекта InputMediaPhoto
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": photo_id}
    result = request_to_api(url=url, querystring=querystring)
    pattern = r'"baseUrl":(.+?),"imageId"'
    find = re.findall(pattern=pattern, string=result)
    photos = list()
    count = 0
    for photo in find:
        if count == int(quantity):
            break
        elif count == 0:
            photo = re.sub(r'{size}', 'z', photo)
        elif count == 1 or count == 2 or count == 3:
            photo = re.sub(r'{size}', 'y', photo)
        photos.append(InputMediaPhoto(media=photo[1:-1]))
        count += 1
    return photos



