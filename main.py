from pprint import pprint
from config import TOKEN_YANDEX, id_vk
from drive import create_and_upload_file
from VK import VK
from yandex import Yandex
from data_json import Data


if __name__ == "__main__":
    def backup_photos(vk_id, album_id, count, yandex_token, folder_name, gdrive, data):
        vk = VK(vk_id, album_id, count=count)
        folder = Yandex(yandex_token, folder_name)
        image_list = vk.get_photos()
        infojson = Data(image_list)
        infojson.data_info()
        folder.create_folder()
        folder.upload_image()
        if gdrive == 1:
            create_and_upload_file()
        else:
            pass
        if data == 1:
            print(f'Информация о загруженных фото:')
            pprint(infojson.data_info())
        else:
            pass

    album_vk = input('Для фото профиля введите 0\nДля фото стены введите 1\n')
    photos_count = input('Введите число фотографий для скачивания\n')
    folder_yandex = input('Введите название папки\n')
    google_drive = input('Если нужно загрузить фото на Google Drive, введите 1\nИначе введите 0\n')
    info = input('Если нужно отобразить информацию о фото, введите 1\nИначе введите 0\n')

    backup_photos(id_vk, int(album_vk), int(photos_count), TOKEN_YANDEX, folder_yandex, int(google_drive), int(info))
