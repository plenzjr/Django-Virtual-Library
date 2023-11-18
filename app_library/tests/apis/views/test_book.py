from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from app_library.models import Author, Book, Publisher, Category
from app_account.models import User
from datetime import date


class BookViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='john.doe@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.client.force_authenticate(user=self.user)  # If views require authentication
        self.url = reverse('book-list')

        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.author = Author.objects.create(
            name='George Orwell',
            birthday='1903-06-25',
            country='India'
        )
        self.category = Category.objects.create(name='Fiction')

        self.book_data = {
            'title': '1984',
            'publisher': self.publisher,
            'publish_date': date.today(),
            'isbn': '1234567890123',
            'pages': 328,
            'cover_url': 'http://example.com/1984.jpg',
            'description': 'A dystopian novel by George Orwell.',
        }

        self.book = Book.objects.create(**self.book_data)
        self.book.author.add(self.author)
        self.book.category.add(self.category)

    def test_get_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book(self):
        book_data = {
            'title': 'Animal Farm',
            'publisher': self.publisher.uid,
            'publish_date': '1945-08-17',
            'isbn': '9876543210123',
            'pages': 112,
            'cover_url': 'http://example.com/animal_farm.jpg',
            'description': 'A farm is taken over by its overworked, mistreated animals.',
        }
        response = self.client.post(self.url, book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.latest('created_at').title, book_data['title'])

    def test_filter_books_by_title(self):
        response = self.client.get(self.url, {'title': '1984'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_filter_books_by_author(self):
        response = self.client.get(self.url, {'author': self.author.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_patch_book(self):
        book_data = {
            'description': 'Updated description.',
        }
        response = self.client.patch(
            reverse('book-detail', args=[self.book.uid]), book_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.description, 'Updated description.')

    def test_delete_book(self):
        response = self.client.delete(reverse('book-detail', args=[self.book.uid]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
