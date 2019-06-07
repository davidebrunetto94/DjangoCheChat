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
from CheChatApp.views import is_participants

class IsParticipantsTestCase(TestCase):

    def test_is_participant_correct(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        is_participant = is_participants(chat_id, user.id)
        self.assert_(is_participant, True)


    def test_is_participant_wrong(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        #creo secondo user
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        #chiedo se è partecipante
        is_participant = is_participants(chat_id, user2.id)

        #controllo che renda false
        self.assertEqual(is_participant, False)

