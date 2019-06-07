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


class GetParticipantsTestCase(TestCase):

    #a participant of the chat asks for the list of the participants
    def test_get_participants(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo secondo user chat
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo terzo user chat
        user3 = User.objects.create_user('davideTest3', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        #id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo secondo utente alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user2.id) + '/' + str(chat_id)
        self.client.post(URL)

        # aggiungo terzo utente alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user3.id) + '/' + str(chat_id)
        self.client.post(URL)


        #chiedo la lista utenti e salvo la response
        URL = 'http://127.0.0.1:8000/chat/get/participants/' + str(chat_id)
        true_response = self.client.post(URL)

        chat = Chat.objects.get(id=chat_id)

        response_expected = {
            'state': 'successful',
            'participants': list(chat.participants.values('id', 'username'))
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))

        # someone who's not a participant of the chat asks for the list of the participants
    def test_get_participants_wrong(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo secondo user chat
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo terzo user chat
        user3 = User.objects.create_user('davideTest3', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo secondo utente alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user2.id) + '/' + str(chat_id)
        self.client.post(URL)

        #faccio logout come primo utente e login come terzo
        self.client.logout()
        self.client.login(username='davideTest3', password='ciao12345')

        # chiedo la lista utenti e salvo la response
        URL = 'http://127.0.0.1:8000/chat/get/participants/' + str(chat_id)
        true_response = self.client.post(URL)

        chat = Chat.objects.get(id=chat_id)

        response_expected = {
            'state': 'not a participant'
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))