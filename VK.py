import requests
import time
import datetime

from config import TOKEN_VK


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
        try:
            response = requests.get(url, params={**self.params, **params}).json()
        except requests.ConnectionError as e:
            print("Ошибка подключения:", e)
        except requests.Timeout as e:
            print("Ошибка тайм-аута:", e)
        except requests.RequestException as e:
            print("Ошибка запроса:", e)
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
                    idx = [i for i, each in enumerate(item['sizes']) if item['sizes'][i]['type'] == types[n]][0]
                    if item['sizes'][idx]['type'] == letter:
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
        print(f'Все {len(response['response']['items'])} фото загружены!')
        return image_list
