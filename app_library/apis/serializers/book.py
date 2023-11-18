from rest_framework import serializers
from app_library.models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    This serializer converts Book model instances to JSON format and ensures proper data
    validation for creating or updating Book instances. It excludes 'created_at' and
    'updated_at' fields from the serialized output to not expose these details.
    """

    class Meta:
        model = Book
        exclude = ['created_at', 'updated_at']
