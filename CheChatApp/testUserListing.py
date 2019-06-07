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


class UserListingTestCase(TestCase):

    def test_user_listing(self):
        #creo vari user
        user = User.objects.create_user('davide1', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        user2 = User.objects.create_user('davide2', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        user3 = User.objects.create_user('davide3', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        user4 = User.objects.create_user('davide4', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        user5 = User.objects.create_user('davide5', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        list_username = []
        list_id = []
        for user in User.objects.all():
            list_username.append(user.username)
            list_id.append(user.id)

        response_expected = {
            'user': list_username,
            'id': list_id
        }
        # users/', views.user_listing),
        #chiedo id su user appena creato
        URL = 'http://127.0.0.1:8000/users/'
        true_response = self.client.post(URL)

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))
