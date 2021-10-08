from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import user


class Bot:

    token_bot = ''

    def __init__(self, token=token_bot):
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})

    def user_age_from(self):
        for new_event in self.longpoll.listen():
            if new_event.type == VkEventType.MESSAGE_NEW:
                if new_event.to_me:
                    age_from = new_event.message
                    return age_from

    def user_age_to(self):
        for new_event in self.longpoll.listen():
            if new_event.type == VkEventType.MESSAGE_NEW:
                if new_event.to_me:
                    age_to = new_event.message
                    return age_to

    def get_token(self):
        for new_event in self.longpoll.listen():
            if new_event.type == VkEventType.MESSAGE_NEW:
                if new_event.to_me:
                    token = new_event.message
                    return token

    def main(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text.lower()
                    if request == "привет":
                        self.write_msg(event.user_id, f"Привет, {event.user_id}")
                    elif request == "пока":
                        self.write_msg(event.user_id, "Пока((")
                    elif request == "поиск":
                        self.write_msg(event.user_id, 'начинаем поиск')
                        url = user.User.get_url_token()
                        self.write_msg(event.user_id, f'Перейдите по {str(url)} и согласитесь с разрешениями\n'
                                                 f'Из адресной строки скопируйте токен,'
                                                 f'который начинается со слов'
                                                 f' "access_token=" и до занака "&"\n'
                                                 f'Вставьте токен в данный диалог')
                        token = self.get_token()
                        self.write_msg(event.user_id, 'Введите возраст от(цифра):')
                        age_from = self.user_age_from()
                        self.write_msg(event.user_id, 'Введите возраст до(цифра):')
                        age_to = self.user_age_to()
                        us = user.User(id_user=event.user_id, age_from=age_from, age_to=age_to, token=token)
                        search = us.search_people(us.select_id())
                        photo = us.top_photo(search)
                        user.write_json(photo)
                        self.write_msg(event.user_id, 'Нашлись партнёры по вашим параметрам!')
                        for i in photo:
                            uid, url = i.items()
                            self.write_msg(event.user_id, f'https://vk.com/id{uid[0]},\n')
                            for photos in url[1]:
                                photo_url = list(photos.items())[0][1]
                                self.write_msg(event.user_id, f'Лучшие фото кандидата:\n{photo_url}')
                        self.write_msg(event.user_id, 'Если хочешь продолжить введи - да\n'
                                                 'Если хочешь остановиться введи - нет')
                        for event_2 in self.longpoll.listen():
                            if event_2.type == VkEventType.MESSAGE_NEW:
                                if event_2.to_me:
                                    request = event_2.text.lower()
                                    if request == 'да':
                                        user.User.insert(photo)
                                        search = us.search_people(us.select_id())
                                        photo = us.top_photo(search)
                                        user.write_json(photo)
                                        for i in photo:
                                            uid, url = i.items()
                                            self.write_msg(event_2.user_id, f'https://vk.com/id{uid[0]},\n')
                                            for photos in url[1]:
                                                photo_url = list(photos.items())[0][1]
                                                self.write_msg(event_2.user_id, f'Лучшие фото кандидата:\n{photo_url}')
                                        self.write_msg(event_2.user_id, 'Если хочешь продолжить введи - да\n'
                                                                   'Если хочешь остановиться введи - нет')
                                    elif request == 'нет':
                                        self.write_msg(event_2.user_id, 'Поиск завершен')
                                        break
                    else:
                        self.write_msg(event.user_id, "Если хочешь начать новый поиск пары введи слово 'поиск'")
