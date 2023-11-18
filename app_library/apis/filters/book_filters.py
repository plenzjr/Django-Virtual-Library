from django_filters import rest_framework as dj_filters

from app_library.models import Book


class BookFilterSet(dj_filters.FilterSet):
    """
    FilterSet for BookViewSet.

    Attributes:
        year (django_filters.NumberFilter): Filter by year of publication.
        title (django_filters.CharFilter): Filter by title of book.
        author (django_filters.CharFilter): Filter by author of book.
        category (django_filters.CharFilter): Filter by category of book.
        publisher (django_filters.CharFilter): Filter by publisher of book.
        isbn (django_filters.CharFilter): Filter by ISBN of book.
    """

    year = dj_filters.NumberFilter(
        field_name='published_date',
        lookup_expr='publish_date__year',
        label='Year of publication',
        help_text='Filter by year of publication',
    )
    title = dj_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title of book',
        help_text='Filter by title',
    )
    author = dj_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        label='Author of book',
        help_text='Filter by author',
    )
    category = dj_filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains',
        label='Category of book',
        help_text='Filter by category',
    )
    publisher = dj_filters.CharFilter(
        field_name='publisher__name',
        lookup_expr='icontains',
        label='Publisher of book',
        help_text='Filter by publisher',
    )
    isbn = dj_filters.CharFilter(
        field_name='isbn',
        lookup_expr='icontains',
        label='ISBN of book',
        help_text='Filter by ISBN',
    )

    class Meta:
        model = Book
        fields = ['year', 'title', 'author', 'category', 'publisher', 'isbn']
