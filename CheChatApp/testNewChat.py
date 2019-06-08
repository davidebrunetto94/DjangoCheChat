from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
from CheChatApp.models import Chat
from django.contrib.auth import get_user_model

class NewChatTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client = Client()

    def test_new_chat_wrong(self):
        #login with wrong credentials
        self.client.login(username='davidello', password='ciao12345')

        URL = 'http://127.0.0.1:8000/chat/new/titolo'
        response = self.client.post(URL)

        #check if the response is right
        self.assertContains(response, 'no auth')

    def test_new_chat_right(self):
        #login with right credentials
        self.client.login(username='davideTest', password='ciao12345')

        URL = 'http://127.0.0.1:8000/chat/new/titolo'
        response = self.client.post(URL)
        state = (json.loads(response.content)["state"])
        self.assertEqual(state, 'successful')


    def test_new_chat_owner(self):
        #check if owner of the chat is right
        self.client.login(username='davideTest', password='ciao12345')
        URL = 'http://127.0.0.1:8000/chat/new/titolo'
        user = User.objects.get(username='davideTest')
        response = self.client.post(URL)
        owner_id = (json.loads(response.content)["owner_id"])
        self.assertEqual(owner_id, user.id)


    def test_new_chat_title(self):
        title = 'titolo'
        self.client.login(username='davideTest', password='ciao12345')
        URL = 'http://127.0.0.1:8000/chat/new/' + title
        user = User.objects.get(username='davideTest')
        response = self.client.post(URL)
        chat_id = (json.loads(response.content)["id"])
        chat_title = chat = Chat.objects.get(id=chat_id).title
        self.assertEqual(title, chat_title)