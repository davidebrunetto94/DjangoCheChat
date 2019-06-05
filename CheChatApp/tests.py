import requests
from django.test import TestCase, Client
from django.contrib.auth.models import User
from CheChatApp.views import login
from CheChatApp.views import logout
from django.shortcuts import render
# Create your tests here.


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        #create user
        user = User.objects.create_user(username='davide', email='davide.brunetto12@gmail.com',password='ciao12345')
        data = {
            "username": "davide",
            "password": "ciao12345",
        }

        URL = 'http://127.0.0.1:8000/'
        request = self.client.post(URL, data=data)
        self.assertContains(request, '''<h1 class="title has-text-link">Che
                <br>Chat</h1>''')