from django.test import TestCase
from app_library.models import Publisher
from app_library.apis.serializers import PublisherSerializer


class PublisherSerializerTests(TestCase):
    def setUp(self):
        self.publisher_attributes = {
            'name': 'Penguin Books'
        }

        self.publisher = Publisher.objects.create(**self.publisher_attributes)
        self.serializer = PublisherSerializer(instance=self.publisher)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['uid', 'name']))

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.publisher_attributes['name'])

    def test_publisher_serialization(self):
        data = self.serializer.data
        expected_data = {
            'uid': str(self.publisher.uid),
            'name': self.publisher_attributes['name']
        }
        self.assertEqual(data, expected_data)

    def test_publisher_deserialization(self):
        data = {
            'name': 'HarperCollins'
        }
        serializer = PublisherSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        publisher = serializer.save()
        self.assertEqual(publisher.name, data['name'])
