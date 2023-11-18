from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from app_library.models import Author
from app_library.apis.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Author instances.

    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions,
    and it only allows the HTTP methods GET, POST, PATCH, and DELETE.
    It also supports filtering Authors based on their name and country.

    Attributes:
        queryset: A QuerySet that is used to retrieve all Author objects.
        serializer_class: The serializer class that should be used for validating
            and deserializing input, and for serializing output.
        http_method_names: A list of allowed HTTP methods for this viewset.
        filter_backends: A list of filter backends to be used for this viewset.
        filterset_fields: A list of fields that should be filterable.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'country']
