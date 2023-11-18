from django.test import TestCase
from django.utils import timezone
from app_library.models import Author


class AuthorModelTests(TestCase):
    def setUp(self):
        self.author_data = {
            'name': 'John Doe',
            'birthday': '1980-05-15',
            'country': 'United States'
        }
        self.author = Author.objects.create(**self.author_data)

    def test_author_creation(self):
        self.assertTrue(isinstance(self.author, Author))
        self.assertEqual(self.author.__str__(), self.author_data['name'])

    def test_author_fields(self):
        self.assertEqual(self.author.name, self.author_data['name'])
        self.assertEqual(str(self.author.birthday), self.author_data['birthday'])
        self.assertEqual(self.author.country, self.author_data['country'])

    def test_author_auto_fields(self):
        self.assertTrue(self.author.created_at <= timezone.now())
        self.assertTrue(self.author.updated_at <= timezone.now())
