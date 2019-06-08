from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
from CheChatApp.models import Chat, PhoneBook


class DeleteContactTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_delete_contact(self):
        # creo user1
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #creo secondo user diverso
        user2 = User.objects.create_user('davide2', 'davide.brunetto12Test@gmail.it', 'password')

        self.client.login(username='davideTest', password='ciao12345')

        #Aggiungo secondo contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user2.id)
        self.client.post(URL)

        #account/contacts/delete/<user_to_delete_id>
        URL = 'http://127.0.0.1:8000/account/contacts/delete/' + str(user2.id)
        true_response = self.client.post(URL)

        response_expected = {'state': 'successful'}

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))

    def test_delete_contact(self):
        # creo user1
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo secondo user diverso
        user2 = User.objects.create_user('davide2', 'davide.brunetto12Test@gmail.it', 'password')

        self.client.login(username='davideTest', password='ciao12345')

        # Aggiungo secondo contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user2.id)
        self.client.post(URL)

        # account/contacts/delete/<user_to_delete_id>
        URL = 'http://127.0.0.1:8000/account/contacts/delete/' + str(user2.id)
        self.client.post(URL)

        phonebook = PhoneBook.objects.get(owner=user)

        contacts_list = phonebook.contacts.values_list('id', flat=True)
        print(contacts_list)
        self.assertQuerysetEqual(contacts_list, User.objects.none())

    def test_delete_contact_phonebook_doesnt_exist(self):
        # creo user1
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        self.client.login(username='davideTest', password='ciao12345')

        #account/contacts/delete/<user_to_delete_id>
        URL = 'http://127.0.0.1:8000/account/contacts/delete/' + str(-1)
        true_response = self.client.post(URL)

        response_expected = {'state': 'phonebook not found'}

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))


    def test_delete_contact_user_doesnt_exist(self):
        # creo user1
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        #creo secondo user diverso
        user2 = User.objects.create_user('davide2', 'davide.brunetto12Test@gmail.it', 'password')

        self.client.login(username='davideTest', password='ciao12345')

        #Aggiungo secondo contatto per creare phonebook
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user2.id)
        self.client.post(URL)


        #Cancello contatto inesistente
        URL = 'http://127.0.0.1:8000/account/contacts/delete/' + str(-1)
        true_response = self.client.post(URL)

        response_expected = {'state': 'user does not exist'}

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))

