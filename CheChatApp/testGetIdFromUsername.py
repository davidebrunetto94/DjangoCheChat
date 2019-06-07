import requests
from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
import datetime
from CheChatApp.views import login
from CheChatApp.models import Chat
from CheChatApp.models import ChatUser
from CheChatApp.views import logout
from django.shortcuts import render


class GetIdFromUsernameTestCase(TestCase):

    def test_id_from_username_correct(self):
        #creo nuovo user
        username = 'davideTest'
        user = User.objects.create_user(username, 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #chiedo id su user appena creato
        URL = 'http://127.0.0.1:8000/users/get/id/' + username
        response = self.client.post(URL)
        response_id = (json.loads(response.content)["id"])

        self.assertEqual(user.id, response_id)

    def test_id_from_username_wrong(self):

        username = 'usernameinesistente'

        URL = 'http://127.0.0.1:8000/users/get/id/' + username
        response = self.client.post(URL)
        response_state = (json.loads(response.content)["state"])

        self.assertEqual(response_state, 'username not found')