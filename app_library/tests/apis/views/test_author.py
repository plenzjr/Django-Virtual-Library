from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from app_library.models import Author
from app_account.models import User


class AuthorViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='john.doe@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.client.force_authenticate(user=self.user)  # If views require authentication
        self.url = reverse('author-list')
        Author.objects.create(
            name='J.K. Rowling',
            birthday='1965-07-31',
            country='United Kingdom'
        )
        Author.objects.create(
            name='George R.R. Martin',
            birthday='1948-09-20',
            country='United States'
        )
        Author.objects.create(
            name='Jane Austen',
            birthday='1775-12-16',
            country='United Kingdom'
        )

    def test_get_authors(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_author(self):
        author_data = {
            'name': 'Ernest Hemingway',
            'birthday': '1899-07-21',
            'country': 'United States'
        }
        response = self.client.post(self.url, author_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 4)
        self.assertEqual(Author.objects.latest('created_at').name, author_data['name'])

    def test_filter_authors_by_name(self):
        response = self.client.get(self.url, {'name': 'J.K. Rowling'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'J.K. Rowling')

    def test_filter_authors_by_country(self):
        response = self.client.get(self.url, {'country': 'United Kingdom'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_patch_author(self):
        author = Author.objects.get(name='J.K. Rowling')
        response = self.client.patch(
            reverse('author-detail', args=[author.uid]), {'country': 'France'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author.refresh_from_db()
        self.assertEqual(author.country, 'France')

    def test_delete_author(self):
        author = Author.objects.get(name='J.K. Rowling')
        response = self.client.delete(reverse('author-detail', args=[author.uid]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 2)
