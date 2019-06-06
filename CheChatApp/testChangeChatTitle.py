import requests
from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
from CheChatApp.views import login
from CheChatApp.models import Chat
from CheChatApp.views import logout
from django.shortcuts import render


class LoginTestCase(TestCase):

    def test_change_chat_title(self):
        #variabile per il nuovo titolo
        newTitle = 'nuovoTitolo'
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        #creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        #id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo il creatore alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user.id) + '/' + str(chat_id)
        self.client.post(URL)

        URL = 'chat/change/title/' + str(user.id) + str(chat_id) + '/' + newTitle
        self.client.post(URL)

        #prendo chat con id
        chat = Chat.objects.get(id=chat_id)

        self.assertEqual(chat.title, newTitle)



