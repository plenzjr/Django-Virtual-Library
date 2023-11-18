from django.test import TestCase
from app_library.models import Author
from app_library.apis.serializers import AuthorSerializer


class AuthorSerializerTests(TestCase):
    def setUp(self):
        self.author_attributes = {
            'name': 'John Doe',
            'birthday': '1980-01-01',
            'country': 'USA',
        }

        self.serializer_data = {
            'name': 'Jane Doe',
            'birthday': '1990-02-02',
            'country': 'Canada',
        }

        self.author = Author.objects.create(**self.author_attributes)
        self.serializer = AuthorSerializer(instance=self.author)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['uid', 'name', 'birthday', 'country']))

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.author_attributes['name'])

    def test_birthday_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['birthday'], '1980-01-01')

    def test_country_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['country'], self.author_attributes['country'])

    def test_author_serialization(self):
        data = self.serializer.data
        self.author_attributes['uid'] = str(self.author.uid)
        self.assertEqual(data, self.author_attributes)

    def test_author_deserialization(self):
        serializer = AuthorSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        author = serializer.save()
        self.assertEqual(author.name, self.serializer_data['name'])
        self.assertEqual(str(author.birthday), self.serializer_data['birthday'])
        self.assertEqual(author.country, self.serializer_data['country'])
