from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
from CheChatApp.models import PhoneBook


class GetContactsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    # user adds another user as a contact
    def test_get_contacts(self):
        # creo user loggato
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # creo secondo user
        user2 = User.objects.create_user('davideTest2', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # creo terzo user
        user2 = User.objects.create_user('davideTest3', 'davide.brunetto12Test@gmail.com', 'ciao12345')

        # aggiungo secondo user come contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user2.id)
        self.client.post(URL)

        # aggiungo terzo user come contatto
        URL = 'http://127.0.0.1:8000/account/contacts/add/' + str(user2.id)
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

    def test_get_contacts_empty(self):
        # creo user loggato
        user = User.objects.create_user('davideTest', 'davide.brunetto12Test@gmail.com', 'ciao12345')
        self.client.login(username='davideTest', password='ciao12345')

        # richiedo lista contatti user
        URL = 'http://127.0.0.1:8000/account/contacts/'
        true_response = self.client.post(URL)

        phonebook = PhoneBook.objects.filter(owner=user)
        response_expected = {
            'contacts': [],
            'state': 'successful'
        }

        self.assertJSONEqual(json.dumps(response_expected), json.loads(true_response.content))
