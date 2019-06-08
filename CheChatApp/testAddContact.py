from django.test import TestCase, Client
from django.contrib.auth.models import User
import json

class AddContactTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    #user adds another user as a contact
    def test_add_contact(self):
        # creo user loggato
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        #creo secondo user
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #aggiungo secondo user come contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user2.id)

        response = self.client.post(URL)
        state = (json.loads(response.content)["state"])

        self.assertEqual(state, 'successful')


    #user adds himself as a contact
    def test_add_same_user_as_contact(self):
        # creo user loggato
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # aggiungo  user come contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user.id)

        response = self.client.post(URL)
        state = (json.loads(response.content)["state"])

        self.assertEqual(state, 'you cannot add yourself')

    #user adds the same contact twice
    def test_add_same_user_as_contact(self):
        # creo user loggato
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')


        #creo secondo user
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # aggiungo secondo user come contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user2.id)
        self.client.post(URL)

        #riaggiungo secondo user come contatto
        response = self.client.post(URL)
        state = (json.loads(response.content)["state"])

        self.assertEqual(state, 'already friend')


    #user adds the same contact twice
    def test_add_contact_user_not_found(self):
        # creo user loggato
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # aggiungo user che non esiste come contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + '-1'
        response = self.client.post(URL)
        state = (json.loads(response.content)["state"])

        self.assertEqual(state, 'user not found')