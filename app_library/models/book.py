from django.db import models
from django.utils.translation import gettext as _

from helpers.models import BaseModel


class Book(BaseModel):
    """
    Model representing a book in the library.

    Attributes:
        title (str): The title of the book.
        author (ManyToManyField): The authors of the book. A book can have multiple authors.
        category (ManyToManyField): The categories associated with the book.
            A book can belong to multiple categories.
        publisher (ForeignKey): The publisher of the book. A book has one publisher.
        publish_date (date): The date when the book was published.
        isbn (str): The International Standard Book Number for the book.
        pages (int): The number of pages in the book.
        cover_url (str): The URL of the book's cover image.
        description (TextField): A text description of the book.
    """

    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
        help_text=_('Book Title')
    )
    author = models.ManyToManyField(
        'app_library.Author',
        blank=True,
        db_column='author_uid',
        verbose_name=_('Author'),
        help_text=_('Book Author'),
        related_name='books'
    )
    category = models.ManyToManyField(
        'app_library.Category',
        blank=True,
        db_column='category_uid',
        verbose_name=_('Category'),
        help_text=_('Book Category'),
        related_name='books'
    )
    publisher = models.ForeignKey(
        'app_library.Publisher',
        on_delete=models.CASCADE,
        db_column='publisher_uid',
        verbose_name=_('Publisher'),
        help_text=_('Book Publisher'),
        related_name='books'
    )
    publish_date = models.DateField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('Publish Date'),
        help_text=_('Book Publish Date')
    )
    isbn = models.CharField(
        blank=True,
        default='',
        max_length=255,
        verbose_name=_('ISBN'),
        help_text=_('Book ISBN')
    )
    pages = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name=_('Pages'),
        help_text=_('Book Pages')
    )
    cover_url = models.CharField(
        blank=True,
        default='',
        max_length=255,
        verbose_name=_('Cover URL'),
        help_text=_('Book Cover URL')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Book Description')
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        ordering = ['title']
        db_table = 'library_book'
