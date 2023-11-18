from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from app_library.models import Publisher
from app_library.apis.serializers import PublisherSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling operations related to Publisher objects.

    This ViewSet allows users to list all publishers, create a new publisher,
    retrieve details of a specific publisher, update a publisher, and delete a publisher.
    Filtering on publisher names is also supported.

    The supported HTTP methods include GET for listing and retrieving, POST for creating,
    PATCH for partially updating, and DELETE for deleting.

    Attributes:
        queryset (QuerySet): The set of publishers to be retrieved.
        serializer_class (PublisherSerializer): The serializer to be used for publishers.
        http_method_names (list): The list of supported HTTP methods.
        filter_backends (list): The list of filter backends to be used.
        filterset_fields (list): The list of fields that can be filtered on.
    """

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
