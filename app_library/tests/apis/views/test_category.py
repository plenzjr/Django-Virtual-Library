from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from app_library.models import Category
from app_account.models import User


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='john.doe@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.client.force_authenticate(user=self.user)  # If views require authentication
        self.url = reverse('category-list')
        Category.objects.create(name='Fiction')
        Category.objects.create(name='Non-fiction')
        Category.objects.create(name='Fantasy')

    def test_get_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_category(self):
        category_data = {
            'name': 'Mystery',
        }
        response = self.client.post(self.url, category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 4)
        self.assertEqual(Category.objects.latest('created_at').name, category_data['name'])

    def test_filter_categories_by_name(self):
        response = self.client.get(self.url, {'name': 'Fiction'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Fiction')

    def test_patch_category(self):
        category = Category.objects.get(name='Fiction')
        response = self.client.patch(
            reverse('category-detail', args=[category.uid]), {'name': 'Science Fiction'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Science Fiction')

    def test_delete_category(self):
        category = Category.objects.get(name='Fiction')
        response = self.client.delete(reverse('category-detail', args=[category.uid]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 2)
