from django.db import models
from django.utils.translation import gettext as _

from helpers.models import BaseModel


class Author(BaseModel):
    """
    Model to represent an author of books in the library.

    Attributes:
        name (str): The name of the author.
        birthday (date): The birthday of the author.
        country (str): The country of origin of the author.
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_('Author Name'),
        help_text=_('Author Name')
    )
    birthday = models.DateField(
        verbose_name=_('Author birthday'),
        help_text=_('Author Birthday')
    )
    country = models.CharField(
        max_length=255,
        verbose_name=_('Author Country'),
        help_text=_('Author Country')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ['name']
        db_table = 'library_author'
