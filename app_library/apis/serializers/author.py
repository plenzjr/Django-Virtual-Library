from rest_framework import serializers
from app_library.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.

    This serializer converts Author model instances to JSON format and validates incoming
    data before creating or updating Author instances. It excludes 'created_at' and 'updated_at'
    fields from serialization.

    """
    class Meta:
        model = Author
        exclude = ['created_at', 'updated_at']
