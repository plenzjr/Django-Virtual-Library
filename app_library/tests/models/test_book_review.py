from datetime import date
from django.test import TestCase
from django.utils import timezone
from app_account.models import User
from app_library.models import Book, BookReview, Publisher


class BookReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='John',
            last_name='Doe'
        )
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.publisher.save()

        self.book = Book.objects.create(
            title='Sample Book',
            publisher=self.publisher,
            publish_date=date.today(),
            isbn='1234567890123',
            pages=100,
            cover_url='http://example.com/sample_book.jpg',
            description='A sample book for testing.'
        )

        self.review_data = {
            'user': self.user,
            'book': self.book,
            'review': 'This is a sample book review.',
            'rating': 4,
        }

        self.book_review = BookReview.objects.create(**self.review_data)

    def test_book_review_creation(self):
        self.assertTrue(isinstance(self.book_review, BookReview))
        expected_str = f"{self.user.full_name}'s review of {self.book.title}"
        self.assertEqual(self.book_review.__str__(), expected_str)

    def test_book_review_fields(self):
        for field, value in self.review_data.items():
            self.assertEqual(getattr(self.book_review, field), value)

    def test_book_review_auto_fields(self):
        self.assertTrue(self.book_review.created_at <= timezone.now())
        self.assertTrue(self.book_review.updated_at <= timezone.now())
