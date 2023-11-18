from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from app_library.models import Category
from app_library.apis.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling operations related to Category objects.

    This ViewSet allows users to list all categories, create a new category,
    retrieve details of a specific category, update a category, and delete a category.
    Filtering on category names is also supported.

    The supported HTTP methods include GET for listing and retrieving, POST for creating,
    PATCH for partially updating, and DELETE for deleting.

    Attributes:
        queryset (QuerySet): The set of categories to be retrieved.
        serializer_class (CategorySerializer): The serializer to be used for categories.
        http_method_names (list): The list of supported HTTP methods.
        filter_backends (list): The list of filter backends to be used.
        filterset_fields (list): The list of fields that can be filtered on.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
