from django.test import TestCase
from app_library.models import Category


class CategoryModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fiction")

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(self.category.__str__(), "Fiction")

    def test_category_fields(self):
        self.assertEqual(self.category.name, "Fiction")

    def test_verbose_name(self):
        self.assertEqual(self.category._meta.verbose_name, 'Category')
        self.assertEqual(self.category._meta.verbose_name_plural, 'Categories')

    def test_ordering(self):
        self.assertEqual(Category._meta.ordering, ['name'])
