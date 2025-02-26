from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from watchlist_app.models import WatchList, StreamPlatform, Review
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            'username': 'testcase',
            'email':  'testcase@example.com',
            'password' : 'test@123',
            'password2': 'test@123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='example@123')

    def test_login(self):
        data = {
            'username': 'example',
            'password': 'example@123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_logout(self):
        response = self.client.post(reverse('login'), {'username': 'example', 'password': 'example@123'})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  