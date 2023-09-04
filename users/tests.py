from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url =  '/api/v1.0/users/registration'

    def test_create_customer(self):
        payload = {
            'username': 'testcustomer',
            'email':'mymail@yahoo.com',
            'password': 'testpassword',
            'birthdate': '1990-01-01',
            'timezone': 'UTC'
        }

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='testcustomer')
        self.assertIsNotNone(user)
        self.assertEqual(user.user_type, 'customer')

    def test_create_customer_fails_without_birthdate_or_tz(self):
        payload = {
            'username': 'customer1',
            'password': 'customer1',
            'email':'mymail@yahoo.com'
           
        }

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

