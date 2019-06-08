from django.test import TestCase, Client
from django.contrib.auth.models import User
import json


class InfoChatByIdTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_info_chat_by_id_single_user(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        #    path('chat/info/<chat_id>', views.info_chat_by_id)
        URL = 'http://127.0.0.1:8000/chat/info/' + str(chat_id)
        true_response = self.client.post(URL)

        # se non si dà il titolo, il titolo sarà stringa vuota
        response_expected = {
            'title': '',
            'isGroup': 'false'
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))

    def test_info_chat_by_id_two_users(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        #creo secondo user
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo secondo user alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user2.id) + '/' + str(chat_id)
        self.client.post(URL)

        #richiedo info chat
        URL = 'http://127.0.0.1:8000/chat/info/' + str(chat_id)
        true_response = self.client.post(URL)

        # se non si dà il titolo, il titolo sarà stringa vuota
        response_expected = {
            'title': '',
            'isGroup': 'false'
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))

    def test_info_chat_by_id_multiple_users(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo secondo user
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo terzo user
        user3 = User.objects.create_user('davideTest3', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo secondo user alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user2.id) + '/' + str(chat_id)
        self.client.post(URL)

        # aggiungo terzo user alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user3.id) + '/' + str(chat_id)
        self.client.post(URL)

        # richiedo info chat
        URL = 'http://127.0.0.1:8000/chat/info/' + str(chat_id)
        true_response = self.client.post(URL)

        # se non si dà il titolo, il titolo sarà stringa vuota
        response_expected = {
            'title': '',
            'isGroup': 'true'
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))

    def test_info_chat_by_id_with_title(self):
        #titolo chat
        title = 'titoloChat'
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo secondo user
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo terzo user
        user3 = User.objects.create_user('davideTest3', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new/' + title
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo secondo user alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user2.id) + '/' + str(chat_id)
        self.client.post(URL)

        # aggiungo terzo user alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user3.id) + '/' + str(chat_id)
        self.client.post(URL)

        # richiedo info chat
        URL = 'http://127.0.0.1:8000/chat/info/' + str(chat_id)
        true_response = self.client.post(URL)

        # se non si dà il titolo, il titolo sarà stringa vuota
        response_expected = {
            'title': title,
            'isGroup': 'true'
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))




