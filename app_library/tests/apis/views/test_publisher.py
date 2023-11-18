from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app_library.models import Publisher
from app_account.models import User


class PublisherViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='john.doe@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.client.force_authenticate(user=self.user)
        self.publisher_data = {'name': 'Penguin Books'}
        self.publisher = Publisher.objects.create(**self.publisher_data)
        self.url = reverse('publisher-list')

    def test_get_publisher_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.publisher_data['name'])

    def test_create_publisher(self):
        new_publisher_data = {'name': 'HarperCollins'}
        response = self.client.post(self.url, new_publisher_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Publisher.objects.count(), 2)
        self.assertEqual(Publisher.objects.latest('created_at').name, new_publisher_data['name'])
