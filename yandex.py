import requests
import json
import time


class Yandex:
    def __init__(self, token, name):
        self.headers = {'Authorization': f'OAuth {token}'}
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.folder_name = name

    def check_folder(self):
        params = {'path': f'{self.folder_name}/', 'fields': 'name'}
        try:
            response = requests.get(f'{self.url}', headers=self.headers, params=params).json()
        except requests.ConnectionError as e:
            print("Ошибка подключения:", e)
        except requests.Timeout as e:
            print("Ошибка тайм-аута:", e)
        except requests.RequestException as e:
            print("Ошибка запроса:", e)
        return response

    def for_folder(self):
        response = self.check_folder()
        try:
            if response['description'] == 'Resource not found.':
                answer = True
        except KeyError:
            if response['name'] == self.folder_name:
                answer = False
        else:
            answer = 'Not identified'
        return answer

    def for_photos(self, file_name, response):
        try:
            if response['description'] == f'Resource "{self.folder_name}/{file_name}" already exists.':
                answer = False
        except KeyError:
            answer = True
        return answer

    def create_folder(self):
        # Проверяем, существует ли уже такая папка
        if self.for_folder():
            params = {'path': self.folder_name}
            try:
                requests.put(self.url, headers=self.headers, params=params)
            except requests.ConnectionError as e:
                print("Ошибка подключения:", e)
            except requests.Timeout as e:
                print("Ошибка тайм-аута:", e)
            except requests.RequestException as e:
                print("Ошибка запроса:", e)
            time.sleep(0.5)
            print('Папка на Яндекс.Диск создана')
        else:
            print('Папка на Яндекс.Диск была создана ранее')

    def upload_image(self):
        with open('info.json', encoding='utf-8') as f:
            image_data = json.load(f)
        for idx, image in enumerate(image_data):
            file_name = image['file_name']
            try:
                response_yandex = requests.get(f'{self.url}/upload', headers=self.headers,
                                               params={'path': f'{self.folder_name}/{file_name}'}).json()
            except requests.ConnectionError as e:
                print("Ошибка подключения:", e)
            except requests.Timeout as e:
                print("Ошибка тайм-аута:", e)
            except requests.RequestException as e:
                print("Ошибка запроса:", e)
            time.sleep(0.5)
            # Проверяем, существуют ли уже такие фото на диске
            if self.for_photos(file_name, response_yandex):
                url_upload = response_yandex['href']
                with open(file_name, 'rb') as file:
                    requests.put(url_upload, files={'file': file})
                    time.sleep(0.5)
                print(f'Фото {idx+1} из {len(image_data)} загружено на Яндекс.Диск...')
            else:
                print(f'Фото {idx+1} из {len(image_data)} уже было загружено на Яндекс.Диск...')
        print(f'Все {len(image_data)} фото загружены!')