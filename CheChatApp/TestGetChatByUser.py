from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
from CheChatApp.models import Chat


class GetChatByUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_chat_by_user_single_chat(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        self.client.post(URL)

        # Invio richiesta
        URL = 'http://127.0.0.1:8000/user/chat/'
        true_response = self.client.post(URL)

        chat = Chat.objects.filter(participants__in=str(user.id)).order_by('-created')

        response_expected = {
            'state': 'successful',
            'chat': list(chat.values('id'))
        }



    def test_get_chat_by_user_multiple_chats(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo nuova chat 1
        URL = 'http://127.0.0.1:8000/chat/new'
        self.client.post(URL)

        # creo nuova chat 2
        URL = 'http://127.0.0.1:8000/chat/new'
        self.client.post(URL)

        # Invio richiesta
        URL = 'http://127.0.0.1:8000/user/chat/'
        true_response = self.client.post(URL)

        chat = Chat.objects.filter(participants__in=str(user.id)).order_by('-created')

        response_expected = {
            'state': 'successful',
            'chat': list(chat.values('id'))
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))

    def test_get_chat_by_user_none(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # Invio richiesta
        URL = 'http://127.0.0.1:8000/user/chat/'
        true_response = self.client.post(URL)

        chat = Chat.objects.filter(participants__in=str(user.id)).order_by('-created')

        response_expected = {
            'state': 'no chat found'
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))


