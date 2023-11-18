from rest_framework import serializers
from app_library.models import BookReview


class BookReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for BookReview model.

    Converts BookReview model instances to JSON format and ensures proper data validation
    for creating or updating BookReview instances. The 'created_at' and 'updated_at' fields
    are excluded from the serialized output.
    """

    class Meta:
        model = BookReview
        exclude = ['created_at', 'updated_at']
