from django.test import TestCase
from app_library.models import Book, BookReview, Publisher
from app_account.models import User
from app_library.apis.serializers import BookReviewSerializer
from datetime import date


class BookReviewSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='john.doe@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.publisher.save()

        self.book = Book.objects.create(
            title='Sample Book',
            publish_date=date.today(),
            publisher=self.publisher,
            isbn='1234567890123',
            pages=100,
            cover_url='http://example.com/sample_book.jpg',
            description='A sample book for testing.'
        )

        self.book_review_attributes = {
            'user': self.user,
            'book': self.book,
            'review': 'This is a sample book review.',
            'rating': 4,
        }

        self.serializer_data = {
            'user': self.user.uid,
            'book': self.book.uid,
            'review': 'This is another sample book review.',
            'rating': 5,
        }

        self.book_review = BookReview.objects.create(**self.book_review_attributes)
        self.serializer = BookReviewSerializer(instance=self.book_review)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['uid', 'user', 'book', 'review', 'rating']))

    def test_review_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['review'], self.book_review_attributes['review'])

    def test_rating_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['rating'], self.book_review_attributes['rating'])

    def test_book_review_serialization(self):
        data = self.serializer.data
        expected_data = {
            'uid': str(self.book_review.uid),
            'user': self.user.uid,
            'book': self.book.uid,
            'review': self.book_review_attributes['review'],
            'rating': self.book_review_attributes['rating'],
        }
        self.assertEqual(data, expected_data)

    def test_book_review_deserialization(self):
        serializer = BookReviewSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        book_review = serializer.save()
        self.assertEqual(book_review.user.uid, self.serializer_data['user'])
        self.assertEqual(book_review.book.uid, self.serializer_data['book'])
        self.assertEqual(book_review.review, self.serializer_data['review'])
        self.assertEqual(book_review.rating, self.serializer_data['rating'])
