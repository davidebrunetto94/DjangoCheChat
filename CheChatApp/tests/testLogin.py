from django.test import TestCase, Client
from django.contrib.auth.models import User


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


    def test_wrong_login(self):
        #test the login with wrong username and password
        #create user
        user = User.objects.create_user(username='davide', email='davide.brunetto12@gmail.com',password='ciao12345')
        data = {
            "username": "davide2",
            "password": "passwordfinta",
        }

        URL = 'http://127.0.0.1:8000/'
        request = self.client.post(URL, data=data)
        self.assertContains(request, 'Wrong credentials</div>')


    def test_wrong_username(self):
        #test the login with wrong username and password
        #create user
        user = User.objects.create_user(username='davide', email='davide.brunetto12@gmail.com',password='ciao12345')
        data = {
            "username": "davide2",
            "password": "ciao12345",
        }

        URL = 'http://127.0.0.1:8000/'
        request = self.client.post(URL, data=data)
        self.assertContains(request, 'Wrong credentials</div>')

    def test_wrong_password(self):
        #test the login with wrong username and password
        #create user
        user = User.objects.create_user(username='davide', email='davide.brunetto12@gmail.com',password='ciao12345')
        data = {
            "username": "davide",
            "password": "passwordfinta",
        }

        URL = 'http://127.0.0.1:8000/'
        request = self.client.post(URL, data=data)
        self.assertContains(request, 'Wrong credentials</div>')

