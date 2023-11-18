from rest_framework import serializers
from app_library.models import Publisher


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Publisher model.

    This serializer transforms Publisher model instances into JSON format and ensures proper
    data validation for creating or updating Publisher instances. It also excludes
    'created_at' and 'updated_at' fields from the serialized output.
    """

    class Meta:
        model = Publisher
        exclude = ['created_at', 'updated_at']
