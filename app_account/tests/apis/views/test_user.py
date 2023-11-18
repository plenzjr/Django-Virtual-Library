from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from app_account.models import User


class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'securepassword123'
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('message', response.data)

    def test_register_existing_user(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ActiveUsersViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.active_users_url = reverse('active-users')
        self.admin_user = User.objects.create_superuser('admin@example.com', 'adminpassword123')
        self.active_user = User.objects.create_user(
            'activeuser@example.com',
            'activeuserpassword123',
            first_name='Active',
            last_name='User'
        )
        self.inactive_user = User.objects.create_user(
            'inactiveuser@example.com',
            'inactiveuserpassword123',
            first_name='Inactive',
            last_name='User'
        )
        self.inactive_user.is_active = False
        self.inactive_user.save()

    def test_list_active_users_unauthenticated(self):
        response = self.client.get(self.active_users_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_active_users_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.active_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['email'], self.admin_user.email)
        self.assertEqual(response.data[1]['email'], self.active_user.email)

    def test_list_active_users_as_regular_user(self):
        self.client.force_authenticate(user=self.active_user)
        response = self.client.get(self.active_users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AllUsersViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.all_users_url = reverse('all-users')
        self.admin_user = User.objects.create_superuser('admin@example.com', 'adminpassword123')
        self.regular_user = User.objects.create_user('user@example.com', 'userpassword123')

    def test_list_all_users_unauthenticated(self):
        response = self.client.get(self.all_users_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_all_users_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.all_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_all_users_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.all_users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
