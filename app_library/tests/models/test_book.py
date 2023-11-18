from django.test import TestCase
from app_library.models import Author, Category, Publisher, Book
from django.utils import timezone


class BookModelTests(TestCase):
    def setUp(self):
        # Creating authors
        self.author1 = Author.objects.create(
            name="Author1",
            birthday="1990-01-01",
            country="Country1"
        )
        self.author2 = Author.objects.create(
            name="Author2",
            birthday="1992-01-01",
            country="Country2"
        )

        # Creating categories
        self.category1 = Category.objects.create(name="Category1")
        self.category2 = Category.objects.create(name="Category2")

        # Creating publisher
        self.publisher = Publisher.objects.create(name="Publisher")

        # Creating book
        self.book = Book.objects.create(
            title="Book1",
            publisher=self.publisher,
            publish_date="2000-01-01",
            isbn="1234567890123",
            pages=100,
            cover_url="http://example.com/cover.jpg",
            description="This is a sample book."
        )

        # Adding authors and categories to the book
        self.book.author.add(self.author1, self.author2)
        self.book.category.add(self.category1, self.category2)

    def test_book_creation(self):
        self.assertTrue(isinstance(self.book, Book))
        self.assertEqual(self.book.__str__(), "Book1")

    def test_book_fields(self):
        self.assertEqual(self.book.title, "Book1")
        self.assertQuerySetEqual(
            self.book.author.all(),
            Author.objects.filter(name__in=["Author1", "Author2"]),
            ordered=False
        )
        self.assertQuerySetEqual(
            self.book.category.all(),
            Category.objects.filter(name__in=["Category1", "Category2"]),
            ordered=False
        )
        self.assertEqual(self.book.publisher, self.publisher)
        self.assertEqual(self.book.publish_date, "2000-01-01")
        self.assertEqual(self.book.isbn, "1234567890123")
        self.assertEqual(self.book.pages, 100)
        self.assertEqual(self.book.cover_url, "http://example.com/cover.jpg")
        self.assertEqual(self.book.description, "This is a sample book.")

    def test_book_auto_fields(self):
        self.assertTrue(self.book.created_at <= timezone.now())
        self.assertTrue(self.book.updated_at <= timezone.now())

    def test_verbose_name(self):
        self.assertEqual(self.book._meta.verbose_name, 'Book')
        self.assertEqual(self.book._meta.verbose_name_plural, 'Books')

    def test_ordering(self):
        self.assertEqual(Book._meta.ordering, ['title'])
