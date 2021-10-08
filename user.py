import requests
import json
import time
import db
from urllib.parse import urlencode


conn = db.create_tables()


def write_json(data_to_write):
    with open('top_10_users.json', 'w', encoding='utf-8') as file:
        json.dump(data_to_write, file, ensure_ascii=False, indent=2)


class VKUser:
    def __init__(self, token, id, version='5.131'):
        self.token = token
        self.id = id
        self.version = version
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': self.token,
                  'user_ids': self.id,
                  'v': self.version
                  }
        data = self.get_response(url, params)
        if data.get('response'):
            self.id = data['response'][0]['id']
        elif data.get('error'):
            self.id = 'Неверный id'

    def get_response(self, url, params):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data

    def get_my_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': self.token,
                  'user_ids': self.id,
                  'fields': 'city, sex, bdate, has_photo, relation',
                  'v': self.version
                  }
        data = self.get_response(url, params)
        try:
            if data['response']:
                return data['response'][0]
        except KeyError:
            pass

    def search_users(self, city, sex, age_from, age_to):
        url = 'https://api.vk.com/method/users.search'
        params = {'access_token': self.token,
                  'q': '',
                  'offset': 0,
                  'count': 1000,
                  'fields': 'city, sex, bdate, has_photo, relation, is_closed',
                  'city': city,
                  'country': 1,
                  'sex': sex,
                  'status': 6,
                  'age_from': age_from,
                  'age_to': age_to,
                  'v': self.version,
                  'has_photo': 1
                  }
        data = self.get_response(url, params)
        return data

    def get_photo(self, id, album_id=None):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': self.token,
            'v': self.version,
            'owner_id': id,
            'album_id': 'profile' if album_id is None else album_id,
            'extended': 1
        }
        data = self.get_response(url, params)
        try:
            return data['response']['items']
        except KeyError:
            pass


class User:
    def __init__(self, id_user, age_from, age_to, token):
        self.kate = VKUser(token=token, id=id_user)
        self.data = self.kate.get_my_info()
        try:
            if self.data['sex'] == 1:
                self.sex = 2
            elif self.data['sex'] == 2:
                self.sex = 1
        except KeyError:
            self.sex = int(input('Введите пол партнера/если Ж то цифру 1, если М то цифру 2:'))
        try:
            self.city = self.data['city']['id']
        except KeyError:
            print('Город не выставлен,по умолчанию выставлена Москва')
            self.city = 1
        self.search = self.kate.search_users(city=self.city, sex=self.sex, age_from=age_from, age_to=age_to)

    def search_people(self, elimination_id=[]):
        people = self.search
        address_list = []
        for i in people["response"]["items"]:
            address_dict = {}
            if i["can_access_closed"] and len(address_list) < 10:
                if i["id"] not in elimination_id:
                    address_dict[i["id"]] = "https://vk.com/id" + str(i["id"])
                    address_list.append(address_dict)
        return address_list

    def top_photo(self, candidates):
        for i in candidates:
            user_id = i.keys()
            top_photo = self.kate.get_photo(user_id)
            time.sleep(0.3)
            likes = []
            try:
                for likes_x in top_photo:
                    likes.append(likes_x['likes']['count'])
                likes.sort(reverse=True)
                url_photo = []
                for photo_x in top_photo:
                    if photo_x['likes']['count'] in likes[0:3]:
                        url_photo.append({photo_x['id']: photo_x['sizes'][-1]['url']})
                i['url_photo'] = url_photo[:3]
            except TypeError:
                pass
        return candidates

    @staticmethod
    def insert(arg):
        for i in arg:
            uid, url = i.items()
            insert = db.User(id=uid[0], url_id=uid[1])
            db.session.add(insert)
            db.session.commit()
            for photo in url[1]:
                photo_url = list(photo.items())[0][1]
                insert = db.Photos(user_id=uid[0], photos_url=photo_url)
                db.session.add(insert)
                db.session.commit()

    @staticmethod
    def select_id():
        list_id = []
        for i in db.session.query(db.User.id).all():
            list_id.append(i[0])
        return list_id

    @staticmethod
    def get_url_token():
        auth_url = 'https://oauth.vk.com/authorize'
        auth_params = {
                'client_id': 7956503,
                'redirect_uri': 'https://oauth.vk.com/blank.html',
                'display': 'page',
                'scope': 'friends',
                'response_type': 'token',
        }
        url = '?'.join((auth_url, urlencode(auth_params)))
        return url
