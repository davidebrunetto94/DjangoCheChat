from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
import datetime


class GetUserInfoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    #user asks for his own username
    def test_get_user_info_correct_username(self):
        #creo nuovo user
        username = 'davideTest'
        user = User.objects.create_user(username, 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #login
        self.client.login(username='davideTest', password='ciao12345')
        login_time = datetime.datetime.now().strftime('%d %b %Y')

        #users/get/<user_id>

        #chiedo info user
        URL = 'http://127.0.0.1:8000/users/get/' + str(user.id)
        response = self.client.post(URL)

        #campi della risposta json
        username_response = (json.loads(response.content)["username"])

        self.assertEqual(username, username_response)

    # user asks for someone else's username
    def test_get_user_info_correct_username_for_other_user(self):
        # creo nuovo user
        username = 'davideTest'
        user = User.objects.create_user(username, 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo secondo user
        username2 = 'conema'
        user2 = User.objects.create_user(username2, 'conema@gmail.com', 'prova')

        # login col secondo utente
        self.client.login(username=username2, password='prova')
        login_time_second_user = datetime.datetime.now().strftime('%d %b %Y')

        #logout
        self.client.logout()

        # login col primo utente
        self.client.login(username='davideTest', password='ciao12345')

        # users/get/<user_id>

        # chiedo info user
        URL = 'http://127.0.0.1:8000/users/get/' + str(user2.id)
        response = self.client.post(URL)

        # campi della risposta json
        username_response = (json.loads(response.content)["username"])
        last_login_response = (json.loads(response.content)["lastlogin"])

        self.assertEqual(username2, username_response) and self.assertEqual(login_time_second_user, last_login_response)

        # user asks for his own login
    def test_get_user_info_correct_login(self):
        # creo nuovo user
        username = 'davideTest'
        user = User.objects.create_user(username, 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # login
        self.client.login(username='davideTest', password='ciao12345')
        login_time = datetime.datetime.now().strftime('%d %b %Y')

        # users/get/<user_id>

        # chiedo info user
        URL = 'http://127.0.0.1:8000/users/get/' + str(user.id)
        response = self.client.post(URL)

        # campo della risposta json
        last_login_response = (json.loads(response.content)["lastlogin"])

        self.assertEqual(login_time, last_login_response)

    # user asks for someone else's login
    def test_get_user_info_correct_login_for_other_user(self):
        # creo nuovo user
        username = 'davideTest'
        user = User.objects.create_user(username, 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo secondo user
        username2 = 'conema'
        user2 = User.objects.create_user(username2, 'conema@gmail.com', 'prova')

        # login col secondo utente
        self.client.login(username=username2, password='prova')
        login_time_second_user = datetime.datetime.now().strftime('%d %b %Y')

        #logout
        self.client.logout()

        # login col primo utente
        self.client.login(username='davideTest', password='ciao12345')

        # users/get/<user_id>

        # chiedo info user
        URL = 'http://127.0.0.1:8000/users/get/' + str(user2.id)
        response = self.client.post(URL)

        # campo della risposta json
        last_login_response = (json.loads(response.content)["lastlogin"])

        self.assertEqual(login_time_second_user, last_login_response)

        # user asks for user that doesn't exist
    def test_get_user_info_user_doesnt_exist(self):
        # creo nuovo user
        username = 'davideTest'
        user = User.objects.create_user(username, 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # login
        self.client.login(username='davideTest', password='ciao12345')
        login_time = datetime.datetime.now().strftime('%d %b %Y')

        # users/get/<user_id>

        # chiedo info user
        URL = 'http://127.0.0.1:8000/users/get/' + str(-1)
        response = self.client.post(URL)

        # campo della risposta json
        state = (json.loads(response.content)["state"])

        self.assertEqual(state, 'user not found')