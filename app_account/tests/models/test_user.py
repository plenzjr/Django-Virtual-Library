from django.test import TestCase
from django.utils import timezone

from app_account.models import User


class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='testpassword123'
        )

    def test_user_creation(self):
        self.assertIsNotNone(self.user.uid)
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'john.doe@example.com')

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), 'John Doe')

    def test_full_name(self):
        self.user.save()
        self.assertEqual(self.user.full_name, 'John Doe')

    def test_soft_delete_user(self):
        self.user.delete()
        self.assertFalse(self.user.is_active)
        self.assertIsNotNone(self.user.inactivation_date)
        self.assertTrue(self.user.inactivation_date <= timezone.now())

    def test_user_manager_create_user(self):
        user = User.objects.create_user(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@example.com',
            password='testpassword123'
        )
        self.assertIsNotNone(user.uid)
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'jane.doe@example.com')

    def test_user_manager_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
