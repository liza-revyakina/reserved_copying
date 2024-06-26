import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def create_and_upload_file():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    try:
        drive = GoogleDrive(gauth)
        with open('info.json', encoding='utf-8') as f:
            image_data = json.load(f)
        for idx, image in enumerate(image_data):
            file_name = image['file_name']
            my_file = drive.CreateFile({'title': f'{file_name}'})
            my_file.SetContentFile(file_name)
            my_file.Upload()

            print(f'Файл {file_name} загружен на GoogleDrive...')
    except Exception as _ex:
        print('Возникла ошибка')

