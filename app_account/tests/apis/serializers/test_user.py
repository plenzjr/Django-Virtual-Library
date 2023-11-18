from django.test import TestCase
from rest_framework.exceptions import ValidationError

from app_account.apis.serializers import RegisterSerializer, UserSerializer
from app_account.models import User


class RegisterSerializerTests(TestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'securepassword123'
        }

        self.serializer_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.com',
            'password': 'securepassword123'
        }

    def test_register_serializer(self):
        serializer = RegisterSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsNotNone(user.uid)
        self.assertEqual(user.first_name, self.serializer_data['first_name'])
        self.assertEqual(user.last_name, self.serializer_data['last_name'])
        self.assertEqual(user.email, self.serializer_data['email'])

    def test_register_serializer_with_existing_email(self):
        User.objects.create_user(**self.user_data)
        serializer = RegisterSerializer(data=self.serializer_data)
        serializer.initial_data['email'] = self.user_data['email']  # existing email
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class UserSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            password='securepassword123'
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_user_serializer(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {'uid', 'first_name', 'last_name', 'email', 'is_active', 'is_staff'}
        )
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['is_active'], self.user.is_active)
        self.assertEqual(data['is_staff'], self.user.is_staff)
