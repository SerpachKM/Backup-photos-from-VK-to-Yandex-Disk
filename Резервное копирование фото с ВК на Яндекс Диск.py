'''Модули'''
import requests
import os
import json
import time


def delete_temporary(directory):
    '''Данный код является функцией которая удаляет все временные файлы и директории из указанного пути.
    Функция принимает один аргумент - путь к директории, которую нужно очистить от временных файлов.
    Внутри функции происходит обход всех файлов и директорий в этой директории с помощью функции os.listdir(),
    затем удаляются каждый файл и директория с помощью функций os.remove() и os.rmdir().'''
    print('Удаление временных файлов и папки.')
    for file_path in os.listdir(directory):
        os.remove(directory + file_path)
    os.rmdir(directory)
    print('Все временные файлы и папки удалены')
    return


class VkUser:
    '''Это код для класса VkUser, который используется для работы с API VK. Он содержит три атрибута: url, params и owner_id.
    Атрибут url содержит URL-адрес API VK, атрибут params содержит параметры запроса, а атрибут owner_id содержит идентификатор владельца.
    Класс VkUser определяет конструктор, который принимает три аргумента: token, version и owner_id.
    Затем конструктор создает объект params с параметрами запроса и сохраняет их в атрибуте params.
    После этого конструктор сохраняет идентификатор владельца в атрибуте owner_id.
    Таким образом, класс VkUser позволяет работать с API VK и получать данные о пользователях, группах и других объектах социальной сети.'''
    url = 'https://api.vk.com/method'

    def __init__(self, token, version, owner_id):
        self.params = {
            'access_token': token,
            'v': version
        }
        self.owner_id = owner_id

    def get_photos(self, q, directory):
        '''Данный код является частью библиотеки для работы с VK API. Функция `get_photos` принимает два аргумента: `q` и `directory`.
        В строке 1 функция `print` выводит сообщение о сохранении фотографий с VK.com во временную папку.
        Строки 2-4 содержат параметры запроса на получение фотографий из VK. Эти параметры включают идентификатор владельца альбома (owner_id) и идентификатор альбома (album_id).
        Параметр extended установлен в значение 1, что означает, что будут получены расширенные данные о фотографиях.
        В строках 5-6 происходит получение данных о фотографиях с помощью метода GET запроса.
        Результатом выполнения запроса является словарь, содержащий информацию о фотографиях, которые были получены.
        Далее в цикле for происходит обработка каждой фотографии и добавление ее в словарь `photos_dict`.
        Если файл уже был добавлен в словарь и его количество лайков отличается от текущего, то происходит обновление имени файла. В противном случае имя файла остается прежним.
        После обработки всех фотографий функция возвращает словарь `photos_dict`, содержащий информацию обо всех полученных фотографиях.'''
        print('Сохранение фотографий с vk.com во временную локальную папку.')
        photos_get_url = self.url + '/photos.get'
        photos_get_params = {
            'owner_id': self.owner_id,
            'album_id': 'profile',
            'extended': '1'
        }
        req = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()

        photos_dict = []
        for photo in req['response']['items']:
            p = {}
            if photo['likes']['count'] not in photos_dict:
                p['file_name'] = str(photo['likes']['count']) + ".jpg"
            else:
                p['file_name'] = str(photo['likes']['count']) + '_' + str(photo['date']) + ".jpg"
            photos_dict.append(photo['likes']['count'])

            max_photo = photo['sizes'][-1]
            p['size'] = max_photo['height']
            img_data = requests.get(max_photo['url']).content
            with open(directory + p['file_name'], 'wb') as handler:
                handler.write(img_data)

        print('Фотографии сохранены на локальном диске.')

        return


class YaUploader:
    '''В данном коде создается класс YaUploader, который предназначен для работы с Яндекс.Диском.
    В классе определены два атрибута - token и directory, которые содержат токен доступа и директорию для загрузки файлов.
    Также определен метод apibaseurl, который содержит базовый URL API Яндекс.Диска. '''
    def __init__(self, token, directory):
        self.token = token
        self.directory = directory
        self.apibaseurl = 'https://cloud-api.yandex.net/v1/disk/resources'

    def create_folder(self):
        '''В данном коде определяется метод create_folder класса YaUploader для создания директории на Яндекс.Диске.
        Метод принимает объект YaUploader в качестве аргумента и создает директорию, если она еще не существует.
        Для этого используется метод get запроса на API Яндекс.Диска, чтобы проверить наличие папки.
        Если папка уже существует, то вызывается метод delete для удаления старой папки. Затем вызывается метод put для создания новой папки.'''
        resp = requests.get(self.apibaseurl, headers={"Authorization": self.token}, params={"path": self.directory})
        if resp.status_code == 200:
            resp = requests.delete(self.apibaseurl, headers={"Authorization": self.token}, params={"path": self.directory})
            time.sleep(2)
            print('Удалена папка на яндекс диске:', directory)

        print('Создание папки на яндекс диске.')
        resp = requests.put(self.apibaseurl, headers={"Authorization": self.token}, params={"path": self.directory})

    def upload(self, kol):
        '''Данный код определяет функцию upload класса YaUploader. Функция принимает объект YaUploader и список файлов для загрузки на Яндекс.Диск.
        Сначала функция создает объект headers, который содержит заголовки запроса. Затем она обходит список файлов с помощью цикла for и проверяет, завершается ли каждый файл на ".jpg".
        Если это так, то функция создает словарь d, который содержит информацию о файле, такую как имя файла и его размер.
        Затем функция добавляет информацию о каждом файле в словарь file_list, который будет использоваться для отправки данных на API Яндекс.Диска.
        После этого функция отправляет данные на API с помощью метода post запроса с помощью библиотеки requests.'''
        headers = {"Authorization": self.token}
        file_list = []
        for file_path in os.listdir(self.directory):
            if file_path.endswith(".jpg"):
                d = {}
                d['file_name'] = file_path
                d['size'] = int(os.path.getsize(self.directory + file_path))
                file_list.append(d)

                def myfunc(file):
                    '''Этот код написан на языке Python и использует библиотеку requests для отправки запросов на API и библиотеку os для работы с файлами и директориями на компьютере.
                    В коде определены две функции: upload и myfunc. Функция upload принимает список файлов для загрузки и отправляет их на API Яндекс.Дисска с помощью метода put запроса.
                    Функция myfunc принимает имя файла и возвращает его размер в байтах.
                    Далее, в функции upload происходит проверка наличия файла на диске и его размера.
                    Если файл существует и его размер меньше или равен заданному значению, то он загружается на диск с помощью метода get запроса.
                    Если файл не существует или его размер больше заданного значения, то он не загружается.
                    После загрузки файла на диск, функция upload отправляет запрос на загрузку файла на сервер с помощью метода post запроса. '''
                    return int(os.path.getsize(self.directory + file))
                if d['file_name'] in sorted(os.listdir(self.directory), key=myfunc, reverse=True)[:kol]:
                    params = {"path": self.directory + file_path}
                    resp = requests.get(self.apibaseurl + '/upload', headers=headers, params=params)

                    with open(self.directory + file_path, 'rb') as f:
                        print('Загрузка файла:', file_path)
                        response = requests.post(resp.json()['href'], files={"file": f})
                        if response.status_code == 201:
                            print('Файл успешно загружен.')
                        else:
                            print('Файл не загружен.')

                    with open(directory + 'file_list.json', 'a') as f:
                        json.dump(d, f)

        print('Загрузка файла json с названиями и размерами файлов')
        params = {"path": self.directory + 'file_list.json'}
        resp = requests.get(self.apibaseurl + '/upload', headers=headers, params=params)

        with open(self.directory + 'file_list.json', 'rb') as f:
            response = requests.post(resp.json()['href'], files={"file": f})
            if response.status_code == 201:
                print('Файл успешно загружен.')
            else:
                print('Файл не загружен.')

        print('Загрузка выполнена.')


if __name__ == "__main__":
    '''Этот код выполняет резервное копирование фотографий. Сначала пользователь вводит данные для авторизации в VK, а затем вводит количество фотографий для копирования. 
    Далее, пользователь вводит Яндекс-токен для загрузки фото на Яндекс-Диск. Затем создается временная папка на локальном диске для хранения фотографий, и фотографии копируются в эту папку с использованием класса VkUser. 
    После копирования фотографий на Яндекс-диск, временная папка удаляется с помощью функции delete_temporary.'''
    token_vk = '0000'
    owner_id = str(input('Введите id аккаунта:\n'))
    directory = 'photos_from_vk/'

    kol = int(input('Введите количество фотографий:\n'))
    token_ya = str(input('Введите яндекс токен:\n'))
    vk_client = VkUser(token_vk, '5.131', owner_id)

    print('Создание временной папки на локальном диске.')
    os.mkdir(directory)
    uploader = YaUploader(token_ya, directory)

    try:
        vk_client.get_photos(requests, directory)
        uploader.create_folder()
        uploader.upload(kol)
    finally:
        delete_temporary(directory)

    print('Все необходимые действия выполнены. Резервное копирование фотографий завершено.')