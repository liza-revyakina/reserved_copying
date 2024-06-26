import requests
import json
from pprint import pprint
from config import TOKEN_YANDEX


class Yandex:
    def __init__(self, token):
        self.headers = {'Authorization': f'OAuth {token}'}
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def check_folder(self, name: str):
        params = {'path': f'{name}/', 'fields': 'name'}
        response = requests.get(f'{self.url}', headers=self.headers, params=params).json()
        return response


def for_folder(folder_name):
    yan = Yandex(TOKEN_YANDEX)
    response = (yan.check_folder(folder_name))
    try:
        if response['description'] == 'Resource not found.':
            answer = True
    except KeyError:
        if response['name'] == folder_name:
            answer = False
    else:
        answer = 'Not identified'
    return answer


def for_photos(file_name, folder_name, response):
    try:
        if response['description'] == f'Resource "{folder_name}/{file_name}" already exists.':
            answer = False
    except KeyError:
        answer = True
    return answer


# pprint(for_return('Image'))
# pprint(for_photos("23.jpg"))