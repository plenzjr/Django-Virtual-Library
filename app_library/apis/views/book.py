from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from app_library.models import Book
from app_library.apis.serializers import BookSerializer
from app_library.apis.filters import BookFilterSet


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling operations related to Book objects.

    It supports listing all books, creating a new book, retrieving a specific book,
    updating a book, and deleting a book. Filtering on book fields is also supported,
    and the specific fields and filter operations are defined in the BookFilterSet class.

    Only authenticated users can create, update, or delete books. However, any user,
    authenticated or not, can view the list of books or details of a specific book.

    Attributes:
        permission_classes (list): The list of permissions required to access this view.
        queryset (QuerySet): The set of books to be retrieved.
        serializer_class (BookSerializer): The serializer to be used for books.
        http_method_names (list): The list of supported HTTP methods.
        filter_backends (list): The list of filter backends to be used.
        filterset_class (BookFilterSet): The class used for filtering the books.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilterSet
