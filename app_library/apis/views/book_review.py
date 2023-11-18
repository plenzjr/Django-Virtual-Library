from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from app_library.models import BookReview
from app_library.apis.serializers import BookReviewSerializer


class BookReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling operations related to BookReview objects.

    It supports listing all book reviews, creating a new book review,
    retrieving a specific book review, updating a book review, and deleting a book review.
    Filtering on 'book' and 'rating' fields is also supported.

    Attributes:
        queryset (QuerySet): The set of book reviews to be retrieved.
        serializer_class (BookReviewSerializer): The serializer to be used for book reviews.
        http_method_names (list): The list of supported HTTP methods.
        filter_backends (list): The list of filter backends to be used.
        filterset_fields (list): The list of fields that can be used for filtering.
    """

    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book', 'rating']
