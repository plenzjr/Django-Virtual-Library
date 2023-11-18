from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from app_library.models import BookReview, Book, Publisher
from app_account.models import User
from datetime import date


class BookReviewViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='john.doe@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('bookreview-list')

        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.publisher.save()

        self.book1 = Book.objects.create(
            title='Sample Book 1',
            publish_date=date.today(),
            publisher=self.publisher,
            isbn='1234567890123',
            pages=100,
            cover_url='http://example.com/sample_book_1.jpg',
            description='A sample book for testing 1.'
        )
        self.book2 = Book.objects.create(
            title='Sample Book 2',
            publish_date=date.today(),
            publisher=self.publisher,
            isbn='1234567890321',
            pages=100,
            cover_url='http://example.com/sample_book_2.jpg',
            description='A sample book for testing 2.'
        )

        BookReview.objects.create(
            user=self.user,
            book=self.book1,
            review='Great book',
            rating=5
        )
        BookReview.objects.create(
            user=self.user,
            book=self.book2,
            review='Good book',
            rating=4
        )

    def test_get_book_reviews(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_review(self):
        review_data = {
            'user': self.user.uid,
            'book': self.book1.uid,
            'review': 'Amazing book',
            'rating': 5
        }
        response = self.client.post(self.url, review_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookReview.objects.count(), 3)
        self.assertEqual(BookReview.objects.latest('created_at').review, review_data['review'])

    def test_filter_book_reviews_by_book(self):
        response = self.client.get(self.url, {'book': self.book1.uid})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['review'], 'Great book')

    def test_filter_book_reviews_by_rating(self):
        response = self.client.get(self.url, {'rating': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['rating'], 5)

    def test_patch_book_review(self):
        review = BookReview.objects.get(review='Great book')
        response = self.client.patch(
            reverse('bookreview-detail', args=[review.uid]), {'rating': 4}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.rating, 4)

    def test_delete_book_review(self):
        review = BookReview.objects.get(review='Great book')
        response = self.client.delete(reverse('bookreview-detail', args=[review.uid]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BookReview.objects.count(), 1)
