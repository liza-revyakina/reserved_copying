import requests
import json
import time
import datetime

from pprint import pprint
from config import TOKEN_VK, TOKEN_YANDEX, id_vk
from yandex_folder import for_folder, for_photos
from drive import create_and_upload_file


class VK:
    def __init__(self, user_id, album, count=5, version='5.131'):
        albums = ['profile', 'wall']
        self.album_id = albums[album]
        self.token = TOKEN_VK
        self.id = user_id
        self.count = count
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': self.album_id, 'rev':  1,
                  'extended': 1, 'photo_sizes': 1, 'count': self.count}
        response = requests.get(url, params={**self.params, **params}).json()
        time.sleep(0.5)
        types = ['w', 'z', 'y', 'x', 'm', 's']
        image_list = []
        file_names = []
        for i, item in enumerate(response['response']['items']):
            # Создание имени файла
            if str(f'{item['likes']['count']}.jpg') in file_names:
                timestamp = item['date']
                value = datetime.datetime.fromtimestamp(timestamp)
                file_name = str(f'{item['likes']['count']}({value.strftime('%Y-%m-%d')}).jpg')
            else:
                file_name = str(f'{item['likes']['count']}.jpg')
                file_names.append(file_name)
            # Выборка фото с самым большим разрешением (по высоте или по типу)
            height = [each['height'] for i, each in enumerate(item['sizes'])]
            if max(height) == 0:
                for n, letter in enumerate(types):
                    idx = [i for i, each in enumerate(item['sizes']) if item['sizes'][i]['type'] == letter][0]
                    if idx == letter:
                        break
                    else:
                        continue
            else:
                idx = [i for i, each in enumerate(item['sizes']) if item['sizes'][i]['height'] == max(height)][0]
            url_image = item['sizes'][idx]['url']
            # Создание словарей с информацией о фото, добавление в общий список
            image_dict = {'file_name': file_name,
                          'size': item['sizes'][idx]['type']}
            image_list.append(image_dict)
            # Загрузка фото
            image_response = requests.get(url_image)
            with open(file_name, 'wb') as f:
                f.write(image_response.content)
            print(f'Фото {i+1} из {len(response['response']['items'])} загружено...')
        # Создание json-файла с информацией о фото
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(image_list, f, ensure_ascii=False, indent=4)
        with open('info.json', encoding='utf-8') as f:
            json_data = json.load(f)
        print(f'Все {len(response['response']['items'])} фото загружены!')
        print(f'Информация о загруженных фото:')
        pprint(json_data)


class Yandex:
    def __init__(self, token, name):
        self.headers = {'Authorization': f'OAuth {token}'}
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.folder_name = name

    def create_folder(self):
        # Проверяем, существует ли уже такая папка
        if for_folder(self.folder_name):
            params = {'path': self.folder_name}
            requests.put(self.url, headers=self.headers, params=params)
            time.sleep(0.5)
            print('Папка на Яндекс.Диск создана')
        else:
            print('Папка на Яндекс.Диск была создана ранее')

    def upload_image(self):
        with open('info.json', encoding='utf-8') as f:
            image_data = json.load(f)
        for idx, image in enumerate(image_data):
            file_name = image['file_name']
            response_yandex = requests.get(f'{self.url}/upload', headers=self.headers,
                                           params={'path': f'{self.folder_name}/{file_name}'}).json()
            time.sleep(0.5)
            # Проверяем, существуют ли уже такие фото на диске
            if for_photos(file_name, self.folder_name, response_yandex):
                url_upload = response_yandex['href']
                with open(file_name, 'rb') as file:
                    requests.put(url_upload, files={'file': file})
                    time.sleep(0.5)
                print(f'Фото {idx+1} из {len(image_data)} загружено на Яндекс.Диск...')
            else:
                print(f'Фото {idx+1} из {len(image_data)} уже было загружено на Яндекс.Диск...')
        print(f'Все {len(image_data)} фото загружены!')


if __name__ == "__main__":
    def backup_photos(vk_id, album_id, count, yandex_token, folder_name, gdrive):
        vk = VK(vk_id, album_id, count=count)
        folder = Yandex(yandex_token, folder_name)
        vk.get_photos()
        folder.create_folder()
        folder.upload_image()
        if gdrive == 1:
            create_and_upload_file()
        else:
            pass

    album_vk = input('Для фото профиля введите 0\nДля фото стены введите 1\n')
    photos_count = input('Введите число фотографий для скачивания\n')
    folder_yandex = input('Введите название папки\n')
    google_drive = input('Если нужно загрузить фото на Google Drive, введите 1\nИначе введите 0\n')

    backup_photos(id_vk, int(album_vk), int(photos_count), TOKEN_YANDEX, folder_yandex, int(google_drive))
