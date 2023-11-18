from django.test import TestCase
from app_library.models import Category
from app_library.apis.serializers import CategorySerializer


class CategorySerializerTests(TestCase):
    def setUp(self):
        self.category_attributes = {
            'name': 'Fiction'
        }

        self.category = Category.objects.create(**self.category_attributes)
        self.serializer = CategorySerializer(instance=self.category)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['uid', 'name']))

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.category_attributes['name'])

    def test_category_serialization(self):
        data = self.serializer.data
        expected_data = {
            'uid': str(self.category.uid),
            'name': self.category_attributes['name']
        }
        self.assertEqual(data, expected_data)

    def test_category_deserialization(self):
        data = {
            'name': 'Science Fiction'
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, data['name'])
