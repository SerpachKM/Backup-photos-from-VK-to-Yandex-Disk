# Курсовая работа "Резервное копирование"
'''
Программа производит резервное копирование фотографий из профиля Вконтакте с наилучшим качеством на Яндекс диск

Входные данные:
user_id_token.txt   - токен Vk, token Yandex, Id Vk
amount_photo = 5    - количество фотографий для резервного копирования
folder_name_ya      - имя создаваемой папки на Яндекс диске

Выходные данные:
data.json            - файл для вывода списка файлов в формате json
Папка на Яндекс диске с сохраненными фотографиями
'''

'''Модули'''
import requests
import json
from tqdm import tqdm


class VkUser:
    '''Данный код ипользуется для работы с API VK (социальной сетью ВКонтакте).
    Класс имеет три параметра: token (токен доступа), user_ids (идентификаторы пользователей) и amount_photo (количество фотографий).
    В конструкторе класса задаются параметры запроса к API VK.
    Параметр params содержит все необходимые данные для запроса, включая токен доступа, идентификаторы пользователей и версию API. Количество фотографий передается через параметр amount_photo.
    Класс VkUser содержит методы для выполнения различных запросов к API VK, таких как получение списка друзей, фотографий, новостей и т.д.
    Для выполнения запросов используются методы, которые принимают параметры запроса в виде словаря.'''
    url = 'https://api.vk.com/method/'

    def __init__(self, token, user_ids, amount_photo, version):
        self.params = {
            'access_token': token,
            'user_ids': user_ids,
            'v': version
        }
        self.amount_photo = amount_photo

    def get_data_user_vk(self):
        '''Данный код является методом класса VkUser. Метод get_data_user_vk() предназначен для получения данных о пользователе из API VK.
        Сначала создается объект data_url, который содержит URL для выполнения запроса к API.
        Затем создаются параметры запроса data_params, которые содержат все необходимые данные, включая идентификатор владельца (owner_id), идентификатор альбома (album_id) и другие параметры.
        Метод requests.get() используется для выполнения HTTP-запроса к API VK и получения данных в формате JSON.
        Параметры запроса передаются в виде словаря, который объединяет параметры запроса из объекта VkUser и объекта data_params.
        После получения данных из API они возвращаются методом return res['response']['items'].
        Здесь res - это результат выполнения HTTP-запроса, а 'response' и 'items' - это атрибуты объекта 'res', которые содержат данные о запросе и его результатах соответственно.
        Таким образом, метод get_data_user_vk() позволяет получить данные о пользователе VK по его идентификатору и передать их в нужный контекст.'''
        data_url = self.url + 'photos.get'
        data_params = {
            'owner_id': self.params['user_ids'],
            'album_id': 'profile',
            'extended': '1',
            'v': '5.131'
        }

        res = requests.get(data_url, params={**self.params, **data_params}).json()
        return res['response']['items']

    def selection_quality_photo(self, sizes_photo):
        '''Данный код - это метод класса VkUser, предназначенный для выбора наилучшего качества фотографий пользователя.
        В методе selection_quality_photo() определяются параметры качества фотографий.
        Вначале создается переменная quality_photo, которая будет хранить наилучшее качество фотографий.
        Затем выполняется цикл for, где перебираются размеры фотографий по свойству sizes_photo.
        В цикле проверяется, соответствует ли размер фотографии условию quality_photo.
        Если да, то quality_photo присваивается размер фотографии. Также сохраняются тип фотографии (type_photo) и ее URL (url_photo).
        Наконец, метод возвращает значения типа фотографии и URL, которые имеют наилучшее качество.'''
        quality_photo = 0
        for size in sizes_photo:
            if size['height'] * size['width'] >= quality_photo:
                quality_photo = size['height'] * size['width']
                type_photo = size['type']
                url_photo = size['url']
        return type_photo, url_photo

    def data_filtering(self):
        '''Данный код представляет метод data_filtering() класса VkUser. Он предназначен для фильтрации данных с профиля пользователя VK.
        Внутри метода сначала вызывается метод get_data_user_vk(), который получает данные пользователя из API VK по идентификатору пользователя.
        Затем вызывается метод selection_quality_photo(), который выбирает наилучшее качество фотографии и сохраняет его параметры - тип фотографии, ее URL и размер.
        Далее создается пустой список list_photo для хранения выбранных фотографий.
        В цикле for для каждой фотографии из полученных данных user_data выбирается фотография с наилучшим качеством, добавляются ее параметры likes, type и url в список list_photo и возвращается этот список.
        То есть функция data_filtering() выбирает из профиля пользователя VK заданное количество фотографий с наилучшим качеством и добавляет их параметры в список.'''
        # Получаем данные с профиля Vk
        data_user = self.get_data_user_vk()
        # Выбираем заданное amount_photo количество фотографий
        data_user = data_user[:amount_photo]

        list_photo = []
        for item in data_user:
            likes_photo = item['likes']['count']
            # Выбираем фотографию с максимальным качеством
            type_photo, url_photo = self.selection_quality_photo(item['sizes'])
            list_photo.append({'likes': likes_photo, 'type': type_photo, 'url': url_photo})
        return list_photo


def get_list_files(list_photo):
    '''Этот код представляет метод get_list_files() класса VkUser.
    Он принимает список list_photo, содержащий параметры выбранных фотографий, и возвращает два списка: output_list_files и list_files.
    output_list_files содержит информацию о файлах, которые будут загружены на сервер, а list_files - информацию о загруженных файлах.
    Для каждого элемента списка list_photo формируется имя файла file_name и сохраняется в списке files.
    Затем имя файла добавляется в список output_list_files со свойством size, которое содержит размер фотографии в байтах.
    Наконец, формируется список list_files, в который добавляются две пары ключ-значение: file_name (имя файла) и url (URL фотографии).
    Таким образом, функция get_list_files() формирует два списка, которые могут быть использованы для загрузки файлов на сервер и отображения их на странице.'''
    output_list_files = []
    list_files = []
    files = []

    for photo in list_photo:
        index = 0
        # Формируем имя файла
        file_name = str(photo['likes']) + '.jpg'
        # Если имя файла существует добавляем к имени _индекс
        while file_name in files:
            index += 1
            file_name = str(photo['likes']) + '_' + str(index)+'.txt'
        files.append(file_name)
        output_list_files.append({'file_name': file_name, 'size': photo['type']})
        list_files.append({'file_name': file_name, 'url': photo['url']})
    return output_list_files, list_files


class YaUploader:
    '''Данный код представляет класс YaUploader.
    Он содержит только конструктор, который принимает один параметр - токен доступа к API Яндекса.
    В конструкторе создается переменная token, которая будет содержать этот токен.'''
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        '''Данный код представляет метод класса YaUploader, который возвращает заголовки запроса к API Яндекса, необходимые для передачи данных в формате json.
        Метод get_headers() возвращает словарь с тремя ключами: Content-Type, Accept и Authorization. Значение ключа Content-Type задается как 'application/json'.
        Ключ Accept имеет значение 'application/json' и используется для указания типа данных, которые передаются в запросе.
        Значение ключа Authorization формируется на основе токена доступа с помощью функции format() и метода OAuth.'''
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        '''Данный код представляет функцию _get_upload_link() класса YaUploader. Она принимает путь к файлу на диске, который нужно загрузить на Яндекс Диск, и возвращает ссылку на загрузку файла.
        Функция сначала создает URL для загрузки файла, используя URL-адрес upload_url и параметры path и overwrite.
        Затем она использует метод get_headers(), чтобы сформировать заголовки запроса. Параметр headers содержит заголовки Content-Type и Accept, а также заголовок Authorization, который формируется с использованием токена доступа.
        Затем функция отправляет запрос на указанный URL с помощью метода requests.get(). Параметр params включает параметры path и overwrite, которые были переданы в методе.=
        'Если запрос выполнен успешно, то возвращается объект response.json(), который содержит информацию о загрузке файла на Яндекс Диск.
        Эта информация может быть использована для дальнейшей работы с файлом на сервере.'''
        upload_url = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def create_folder_ya(self, folder_name):
        '''Данный код представляет метод create_folder_ya() класса YaUploader, который создает папку на Яндекс Диске.
        Прежде всего, создается URL для создания папки на Яндекс Диске, используя URL upload_url и параметр path, который передает имя папки. Затем формируются заголовки запроса с помощью метода get_headers().
        Параметр overwrite имеет значение false, что означает, что при создании папки будет создана новая папка, если она уже существует.
        Отправляется запрос на создание папки с помощью метода put(). Параметр f'{upload_url}?path={folder_name}' указывает на URL для создания папки и передает параметр path с именем папки.
        Если ответ от сервера успешный (код состояния 201), то выводится сообщение о том, что папка успешно создана на Яндекс Диске с помощью метода print().
        Если же ответ от сервера неудачный, то выводится соответствующее сообщение об ошибке.'''
        upload_url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        headers = self.get_headers()
        params = {'overwrite': 'false'}
        response = requests.put(f'{upload_url}?path={folder_name}', headers=headers, params=params)
        if response.status_code == 201:
            # Логирование процесса записи на яндекс диск
            print(f'Папка {folder_name} успешно создана на Яндекс диске')

    def upload(self, list_files, folder_ya):
        """Данный код является методом upload() класса YaUploader и предназначен для загрузки файлов с сервера на Яндекс Диск.
        Сначала создается папка на Яндекс Диске и выводится сообщение о ее создании на экран.
        Затем в цикле for по каждому файлу из списка list_files вызывается метод _get_upload_link(), который возвращает ссылку на загрузку файла на Яндекс Диск.
        Ссылка сохраняется в переменной response_href, затем вызывается метод put() для загрузки файла на диск.
        После того, как все файлы были загружены, выводится сообщение об успешном сохранении файлов на Яндекс Диск."""
        # создаем папку на яндекс диске
        self.create_folder_ya(folder_name=folder_ya)
        print(f'Cохраняем файлы {len(list_files)} шт. в папку {folder_ya} на Яндекс диск')
        for file in tqdm(list_files,colour='green'):
            file_name = file['file_name']
            disk_file_path = folder_ya + '/' + file_name  # Если папка существует на яндекс диске
            response_href = self._get_upload_link(disk_file_path=disk_file_path)
            href = response_href.get('href', '')
            data = requests.get(file['url'])
            response = requests.put(href, data=data.content)
        print('Файлы успешно сохранены на Яндекс диск')

if __name__ == '__main__':
    '''Данный фрагмент написан на языке Python и представляет собой пример кода для загрузки фотографий из ВКонтакте на Яндекс.Диск с использованием API.
    В начале кода проверяется, является ли текущий скрипт главным модулем (__name__ == "__main__"). 
    Если да, то происходит чтение токенов доступа к ВКонтакте и Яндекс.Диску, а также идентификаторов пользователей из файла "user_id_token.txt". 
    Затем запрашивается количество фотографий, которое необходимо загрузить на Яндекс.Диск, и задается имя папки на Яндекс.Диске.
    Далее создается экземпляр класса VkUser с параметрами, полученными из файла "user_id_token.txt", и с помощью этого класса происходит получение списка фотографий наилучшего качества из ВКонтакте. 
    После этого происходит формирование списков output_list_files и list_files на основе полученных фотографий.
    Наконец, происходит запись списка output_list_files в файл в формате JSON с помощью open() и json.dump(), а затем сохранение списка на Яндекс.Диск с помощью YaUploader().'''
    # Получаем токен Vk, токен на Яндекс диске, user id Vk
    with open('user_id_token.txt', 'r') as file_object:
        token_vk = file_object.readline().strip()
        token_ya = file_object.readline().strip()
        user_ids = file_object.readline().strip()

    # Запрашиваем количество сохраняемых фотографий
    amount_photo = int(input('Введите количество сохраняемых фотографий на Яндекс диск: '))
    # Задаем имя папки  на Яндекс диске
    folder_name_ya = 'my_photo_vk'
    # Задаем версию Vk
    version = '5.131'

    # Создаем экземпляр класса VkUser()
    vk_client = VkUser(token=token_vk, user_ids=user_ids, amount_photo=amount_photo, version=version)
    # Получаем список заданного amount_photo количества фотографий наилучшего качества
    list_photo = vk_client.data_filtering()
    # Формируем списки
    output_list_files, list_files = get_list_files(list_photo)
    # Выводим требуемый список output_list_files в json файл  data.json
    with open('data.json', 'w', encoding='utf-8') as file_obj:
       json.dump(output_list_files, file_obj, indent=4, ensure_ascii=False)
       print('Список файлов с указанием размера сохранен в формате json в файл data.json')

    # Создаем экземпляр класса YaUploader()
    uploader = YaUploader(token_ya)
    # Сохраняем фотографии на Яндекс диск
    uploader.upload(list_files, folder_name_ya)
