from django.test import TestCase
from app_library.models import Author, Publisher, Category, Book
from app_library.apis.serializers import BookSerializer
from datetime import date


class BookSerializerTests(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.publisher.save()

        self.author1 = Author.objects.create(
            name='Author 1',
            birthday='2000-01-01',
            country='Country'
        )
        self.author2 = Author.objects.create(
            name='Author 2',
            birthday='2000-02-02',
            country='Country'
        )
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')

        self.book_attributes = {
            'title': 'Sample Book',
            'publisher': self.publisher,
            'publish_date': date.today(),
            'isbn': '1234567890123',
            'pages': 100,
            'cover_url': 'http://example.com/sample_book.jpg',
            'description': 'A sample book for testing.'
        }

        self.book = Book.objects.create(**self.book_attributes)
        self.book.author.set([self.author1, self.author2])
        self.book.category.set([self.category1, self.category2])

        self.serializer = BookSerializer(instance=self.book)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set([
                'uid',
                'title',
                'author',
                'category',
                'publisher',
                'publish_date',
                'isbn',
                'pages',
                'cover_url',
                'description'
            ])
        )

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.book_attributes['title'])
        self.assertEqual(data['publisher'], self.publisher.uid)
        self.assertEqual(data['publish_date'], self.book_attributes['publish_date'].isoformat())
        self.assertEqual(data['isbn'], self.book_attributes['isbn'])
        self.assertEqual(data['pages'], self.book_attributes['pages'])
        self.assertEqual(data['cover_url'], self.book_attributes['cover_url'])
        self.assertEqual(data['description'], self.book_attributes['description'])
        self.assertEqual(len(data['author']), 2)
        self.assertEqual(len(data['category']), 2)

    def test_book_serialization(self):
        data = self.serializer.data
        expected_data = {
            'uid': str(self.book.uid),
            'title': self.book_attributes['title'],
            'author': [self.author1.uid, self.author2.uid],
            'category': [self.category1.uid, self.category2.uid],
            'publisher': self.publisher.uid,
            'publish_date': self.book_attributes['publish_date'].isoformat(),
            'isbn': self.book_attributes['isbn'],
            'pages': self.book_attributes['pages'],
            'cover_url': self.book_attributes['cover_url'],
            'description': self.book_attributes['description'],
        }
        self.assertEqual(data, expected_data)

    def test_book_deserialization(self):
        data = {
            'title': 'Another Sample Book',
            'author': [self.author1.uid, self.author2.uid],
            'category': [self.category1.uid, self.category2.uid],
            'publisher': self.publisher.uid,
            'publish_date': '2023-10-01',
            'isbn': '9876543210987',
            'pages': 200,
            'cover_url': 'http://example.com/another_sample_book.jpg',
            'description': 'Another sample book for testing.',
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(book.title, data['title'])
        self.assertEqual(book.publisher.uid, data['publisher'])
        self.assertEqual(book.publish_date, date(2023, 10, 1))
        self.assertEqual(book.isbn, data['isbn'])
        self.assertEqual(book.pages, data['pages'])
        self.assertEqual(book.cover_url, data['cover_url'])
        self.assertEqual(book.description, data['description'])
        self.assertEqual(book.author.count(), 2)
        self.assertEqual(book.category.count(), 2)
