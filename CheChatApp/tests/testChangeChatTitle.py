from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
from CheChatApp.models import Chat


class ChangeTitleTestCase(TestCase):
    def setUp(self):
        self.client = Client()

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

        #cambio il titolo
        URL = 'http://127.0.0.1:8000/chat/change/title/' + str(chat_id) + '/' + newTitle
        self.client.post(URL)

        #prendo chat con id
        chat = Chat.objects.get(id=chat_id)

        #controllo che il titolo sia corretto
        self.assertEqual(newTitle, chat.title)


    def test_change_chat_title_not_owner(self):
        #vecchio titolo
        oldTitle = 'vecchioTitolo'

        #variabile per il nuovo titolo
        newTitle = 'nuovoTitolo'
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #login
        self.client.login(username='davideTest', password='ciao12345')
        #creo user diverso
        user2 = User.objects.create_user('davidigno', 'davide.brunetto@gmail.com', 'meleperebanane')

        #creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new/' + oldTitle
        response_creation = self.client.post(URL)

        #id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        #logout
        self.client.logout()
        self.client.login(username='davidigno', password='meleperebanane')

        #cambio il titolo loggato come altro user
        URL = 'http://127.0.0.1:8000/chat/change/title/' + str(chat_id) + '/' + newTitle
        response_change_title = self.client.post(URL)

        #prendo chat con id
        chat = Chat.objects.get(id=chat_id)

        #stato della risposta nel json
        state = (json.loads(response_change_title.content)["state"])

        #controllo che il titolo sia rimasto quello vecchio
        self.assertEqual(state, 'not the owner')





