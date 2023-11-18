from rest_framework import serializers
from app_library.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    Transforms Category model instances to JSON format, ensuring proper data validation
    for creating or updating Category instances. It omits 'created_at' and 'updated_at'
    fields in the serialized output.
    """
    class Meta:
        model = Category
        exclude = ['created_at', 'updated_at']
