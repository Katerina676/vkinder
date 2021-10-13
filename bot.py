from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import user


class Bot:

    token_bot = ''

    def __init__(self, token=token_bot):
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message, attachment = ''):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), 'attachment': attachment})

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
                        user.User.insert(photo)
                        self.write_msg(event.user_id, 'Нашлись партнёры по вашим параметрам!')
                        ids = us.select_id()
                        ids_user = ids[0]
                        top_photos = us.select_photo(ids_user)
                        self.write_msg(event.user_id, f'https://vk.com/id{ids_user},\n')
                        for i in top_photos:
                            self.write_msg(event.user_id, '', attachment=i)
                        self.write_msg(event.user_id, 'Если хочешь продолжить введи +\n'
                                                      'Если хочешь остановиться введи -')
                        for event_2 in self.longpoll.listen():
                            if event_2.type == VkEventType.MESSAGE_NEW:
                                if event_2.to_me:
                                    request = event_2.text.lower()
                                    if request == '+':
                                        ids.pop(0)
                                        if len(ids) != 0:
                                            ids_user = ids[0]
                                            top_photos = us.select_photo(ids_user)
                                            self.write_msg(event_2.user_id, f'https://vk.com/id{ids_user},\n')
                                            for i in top_photos:
                                                self.write_msg(event_2.user_id, '', attachment=i)
                                            self.write_msg(event_2.user_id, 'Если хочешь продолжить введи +\n'
                                                                          'Если хочешь остановиться введи -')
                                        elif len(ids) == 0:
                                            self.write_msg(event_2.user_id, 'Список пуст начать новый поиск?(да/нет)')
                                    elif request == 'да':
                                        search = us.search_people(us.select_id())
                                        photo = us.top_photo(search)
                                        user.write_json(photo)
                                        user.User.insert(photo)
                                        self.write_msg(event_2.user_id, 'Нашлись партнёры по вашим параметрам!')
                                        ids = us.select_id()
                                        ids = ids[-10:]
                                        ids_user = ids[0]
                                        top_photos = us.select_photo(ids_user)
                                        self.write_msg(event_2.user_id, f'https://vk.com/id{ids_user},\n')
                                        for i in top_photos:
                                            self.write_msg(event_2.user_id, '', attachment=i)
                                        self.write_msg(event_2.user_id, 'Если хочешь продолжить введи +\n'
                                                                      'Если хочешь остановиться введи -')
                                    elif request == '-' or 'нет':
                                        self.write_msg(event_2.user_id, 'Поиск завершен')
                                        break
                                    else:
                                        self.write_msg(event_2.user_id, 'Я вас не понял')
                    else:
                        self.write_msg(event.user_id, "Если хочешь начать новый поиск пары введи слово 'поиск'")
