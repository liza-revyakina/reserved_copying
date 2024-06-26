# Резервное копирование

### Функционал
Данная программа скачивает заданное пользователем число последних фото профиля или со стены пользователя (на выбор), называя их в соответствии с количеством лайков на них. После создает папку на Яндекс.Диск с произвольным названием, которое вводит пользователь, и загружает в нее эти фото. Если папка или фото уже были на диске ранее, то об этом сообщается в логах терминала. Далее пользователь может загрузить фото на Google Drive, без создания папки.

### Реализация
В файле main.py содержатся класс VK, который скачивает фото, называет их и создает json-файл с информацией, и класс Yandex, который создает папку и загружает в нее фото на Яндекс Диск. Также там содержится основная исполняемая функция, которая принимает VK.id, тип альбома, количество фото, токен Яндекса и имя папки. Перед запуском функции пользователь вводит данные о типе альбома, количестве фото и имени папки, все токены берутся из config.py.

В файле yandex_folder.py происходит проверка на наличие папки и фото на Яндекс.Диске.

В файле drive.py происходит загрузка фото на Google Drive с помощью библиотеки PyDrive.

В файле config.py хранятся все токены.

### Требования
Для работы основной части программы необходимо добавить токены VK, Яндекса и VK.id в файл config.py. Также для корректной работы при получении токена VK нужно указать в query SCOPE параметр photos, желательно добавить offline, чтобы не обновлять его ежедневно.

Для работы с Google Drive нужно ознакомиться с [документацией PyDrive](https://pythonhosted.org/PyDrive/quickstart.html), пункт *Authentication*, по алгоритму скачать json-файл, переименовать его в *client_secrets.json* и добавить в рабочую директорию.

### Установка requirements.txt
```
$ pip install -r requirements.txt
```