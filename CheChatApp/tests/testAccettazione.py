from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
import requests
import json
from CheChatApp.models import Chat, PhoneBook, Message


class AcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()

    #1
    def test_info_chat_by_id_two_users(self):
        # creo user proprietario chat
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        #creo secondo user
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo nuova chat
        URL = 'http://127.0.0.1:8000/chat/new'
        response_creation = self.client.post(URL)

        # id della chat
        chat_id = (json.loads(response_creation.content)["id"])

        # aggiungo secondo user alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user2.id) + '/' + str(chat_id)
        self.client.post(URL)

        #richiedo info chat
        URL = 'http://127.0.0.1:8000/chat/info/' + str(chat_id)
        true_response = self.client.post(URL)

        chat = Chat.objects.get(id=chat_id)

        # se non si dà il titolo, il titolo sarà stringa vuota
        response_expected = {
            'title': '',
            'isGroup': 'false',
            'lastMessage': chat.lastMessage
        }

        self.assertJSONEqual(json.dumps(response_expected, sort_keys=True,indent=1,cls=DjangoJSONEncoder), json.loads(true_response.content))

    #2
    def test_get_contacts(self):
        # creo user loggato
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo secondo user
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo terzo user
        user3 = User.objects.create_user('davideTest3', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # aggiungo secondo user come contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user2.id)
        self.client.post(URL)

        # aggiungo terzo user come contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user3.id)
        self.client.post(URL)

        #account/contacts/', views.get_contacts)
        #richiedo lista contatti primo user
        URL = 'http://127.0.0.1:8000/account/contacts/'
        true_response = self.client.post(URL)

        phonebook = PhoneBook.objects.get(owner=user)
        response_expected = {
            'state': 'successful',
            'contacts': list(phonebook.contacts.values_list(flat=True))
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))

    #3
    def test_write_message(self):
        user1 = User.objects.create_user('ginoPulcinoTest', 'gino.pulcino@pulcinomail.com', 'ginopulcino')
        user2 = User.objects.create_user('cinoPulginoTest', 'cino.pulgino@pulginomail.com', 'cinopulgino')

        self.client.login(username=user1.username, password=user1.password)

        # aggiungo user2 come contatto
        self.client.post('http://127.0.0.1:8000/account/contacts/add/' + str(user2.id))

        title = 'chat'
        response = self.client.post('http://127.0.0.1:8000/chat/new/' + title)

        chat_id_response = (json.loads(response.content)["id"])

        self.client.post('http://127.0.0.1:8000/chat/add/participant/' + str(user2.id) + '/' + str(chat_id_response))

        # si crea richiesta post
        post_data = {'id': chat_id_response, 'message_body' : 'Hola!'}
        actual_response = self.client.post('http://127.0.0.1:8000/chat/add/message/', data=post_data)
        expected_response = {'state': 'successful', 'message_id' : list(Message.objects.filter(chat=chat_id_response).order_by('-timestamp'))[0].id}

        self.assertJSONEqual(json.dumps(expected_response), json.loads(actual_response.content))



        #4
    def test_new_group_right_json(self):
        title = 'titolo'
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        # login with right credentials
        self.client.login(username='davideTest', password='ciao12345')

        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        user3 = User.objects.create_user('davideTest3', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        URL = 'http://127.0.0.1:8000/chat/new/' + title
        response = self.client.post(URL)
        chat_id_response = (json.loads(response.content)["id"])

        # secondo utente aggiunto alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user2.id) + '/' + str(chat_id_response)
        request = self.client.post(URL)

        # terzo utente aggiunto alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user3.id) + '/' + str(chat_id_response)
        request = self.client.post(URL)

        chat = Chat.objects.get(id=chat_id_response)
        self.assertIsNotNone(chat)
        self.assertEqual(len(chat.participants.values_list()), 3)

        #5
    def test_login(self):
        # create user
        user = User.objects.create_user(username='davide', email='davide.brunetto12@gmail.com',
                                        password='ciao12345')
        data = {
            "username": "davide",
            "password": "ciao12345",
        }

        URL = 'http://127.0.0.1:8000/'
        request = self.client.post(URL, data=data)
        self.assertContains(request, '''<h1 class="title has-text-link">Che
                <br>Chat</h1>''')


        #6
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

        #7
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

        # aggiungo secondo utente alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user_to_add.id) + '/' + str(chat_id)
        self.client.post(URL)

        #chiedo chat
        chat = Chat.objects.filter(id=chat_id)

        self.assertIn(user_to_add.id, list(chat.values_list('participants', flat=True)))

        #8
    def test_leave_group(self):
        user1 = User.objects.create_user('ginoPulcinoTest', 'gino.pulcino@pulcinomail.com', 'ginopulcino')
        user2 = User.objects.create_user('cinoPulginoTest', 'cino.pulgino@pulginomail.com', 'cinopulgino')

        self.client.login(username=user1.username, password=user1.password)

        # aggiungo user2 come contatto
        self.client.post('http://127.0.0.1:8000/account/contacts/add/' + str(user2.id))

        title = 'chat'
        response = self.client.post('http://127.0.0.1:8000/chat/new/' + title)

        chat_id_response = (json.loads(response.content)["id"])

        self.client.post('http://127.0.0.1:8000/chat/add/participant/' + str(user2.id) + '/' + str(chat_id_response))

        response = self.client.post('http://127.0.0.1:8000/chat/delete/participant/' + chat_id_response)

        self.assert_(not Chat.objects.get(id=chat_id_response).participants.filter(id=user1.id).exists())
        self.assertJSONEqual(json.dumps({'state' : 'successful'}), json.loads(response.content))

        #9
    def test_get_participants(self):
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

        # aggiungo terzo utente alla chat
        URL = 'http://127.0.0.1:8000/chat/add/participant/' + str(user3.id) + '/' + str(chat_id)
        self.client.post(URL)

        # chiedo la lista utenti e salvo la response
        URL = 'http://127.0.0.1:8000/chat/get/participants/' + str(chat_id)
        true_response = self.client.post(URL)

        chat = Chat.objects.get(id=chat_id)

        response_expected = {
            'state': 'successful',
            'participants': list(chat.participants.values('id', 'username'))
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))

        #10
    def test_add_contact(self):
        # creo user loggato
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        #creo secondo user
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #aggiungo secondo user come contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user2.id)
        self.client.post(URL)

        #chiedo lista contatti dello user
        URL = 'http://127.0.0.1:8000/account/contacts/'

        #chiedo phonebook dell'user
        phonebook = PhoneBook.objects.filter(owner=user)

        self.assertIn(user2.id, list(phonebook.values_list('contacts', flat=True)))

        #11
    def test_new_chat_right(self):
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        title = 'titolo'
        #login with right credentials
        self.client.login(username='davideTest', password='ciao12345')


        URL = 'http://127.0.0.1:8000/chat/new/' + title
        response = self.client.post(URL)
        chat_id_response = (json.loads(response.content)["id"])

        chat = Chat.objects.get(id=chat_id_response)
        self.assertIsNotNone(chat)

