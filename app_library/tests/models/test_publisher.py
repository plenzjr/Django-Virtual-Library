from django.test import TestCase
from app_library.models import Publisher


class PublisherModelTests(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name="Penguin Books")

    def test_publisher_creation(self):
        self.assertTrue(isinstance(self.publisher, Publisher))
        self.assertEqual(self.publisher.__str__(), "Penguin Books")

    def test_publisher_fields(self):
        self.assertEqual(self.publisher.name, "Penguin Books")

    def test_verbose_name(self):
        self.assertEqual(self.publisher._meta.verbose_name, 'Publisher')
        self.assertEqual(self.publisher._meta.verbose_name_plural, 'Publishers')

    def test_ordering(self):
        self.assertEqual(Publisher._meta.ordering, ['name'])
