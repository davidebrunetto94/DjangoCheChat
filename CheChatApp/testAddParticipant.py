import requests
from django.test import TestCase, Client
from django.contrib.auth.models import User
from CheChatApp.models import Chat
from django.contrib.auth import get_user_model
from CheChatApp.views import login
from CheChatApp.views import logout
from django.shortcuts import render
from django.http import JsonResponse
import json


class AddParticipantTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    #User who created the chat tries to add himself twice. Expected result -> 'user exists'
    def test_add_participant_twice(self):
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

        # tento di aggiungere lo stesso utente alla chat
        request = self.client.post(URL)

        #controllo che il json restituito mi dica che lo user esiste già
        self.assertContains(request, 'user exists')

    #User who created the chat tries to add another user. Expected result -> 'successful'
    def test_add_participant_json(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #creo secondo user diverso
        user_to_add = User.objects.create_user('davide2', 'davide.brunetto12Test@gmail.it', 'password')

        self.client.login(username='davideTest', password='ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo il creatore alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user.id) + '/' + str(chat_id)
        self.client.post(URL)

        # aggiungo secondo utente alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user_to_add.id) + '/' + str(chat_id)
        request = self.client.post(URL)

        # controllo che il json restituito mi dia succesful
        self.assertContains(request, 'successful')


    #User who created the chat tries to add another user.
    def test_add_participant(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #creo secondo user diverso
        user_to_add = User.objects.create_user('davide2', 'davide.brunetto12Test@gmail.it', 'password')

        self.client.login(username='davideTest', password='ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo il creatore alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user.id) + '/' + str(chat_id)
        self.client.post(URL)

        # aggiungo secondo utente alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user_to_add.id) + '/' + str(chat_id)
        self.client.post(URL)

        #chiedo chat
        chat = Chat.objects.filter(id=chat_id)

        self.assertIn(user_to_add.id, list(chat.values_list('participants', flat=True)))

    # User different from the one who created the chat and is not a participant tries to add himself to the chat.
    # Expected result -> 'not a participant'
    def test_add_not_participant(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #creo secondo user diverso
        user_to_add = User.objects.create_user('davide2', 'davide.brunetto12Test@gmail.it', 'password')

        #login come primo user
        self.client.login(username='davideTest', password='ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo il creatore alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user.id) + '/' + str(chat_id)
        self.client.post(URL)

        #logout primo user
        self.client.logout()

        #login secondo user
        self.client.login(username='davide2', password='password')

        # secondo utente aggiunge se stesso alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user_to_add.id) + '/' + str(chat_id)
        request = self.client.post(URL)

        # chiedo chat
        chat = Chat.objects.filter(id=chat_id)

        self.assertNotIn(user_to_add.id, list(chat.values_list('participants', flat=True)))

    # User different from the one who has created and is not a participant the chat tries to add another user
    def test_not_participant_adds_other_user(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo secondo user diverso
        user_2 = User.objects.create_user('davide2', 'davide.brunetto12Test@gmail.it', 'password')

        # creo terzo user
        user_to_add = User.objects.create_user('davide3', 'davide.brunetto12Test@gmail.eu', 'password')

        # login come primo user
        self.client.login(username='davideTest', password='ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo il creatore alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user.id) + '/' + str(chat_id)
        self.client.post(URL)

        # logout primo user
        self.client.logout()

        # login secondo user
        self.client.login(username='davide2', password='password')

        # secondo utente aggiunge altro utente alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user_to_add.id) + '/' + str(chat_id)
        request = self.client.post(URL)

        # chiedo chat
        chat = Chat.objects.filter(id=chat_id)
        self.assertNotIn(user_to_add.id, list(chat.values_list('participants', flat=True)))


