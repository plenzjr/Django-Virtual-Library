from django.db import models
from django.utils.translation import gettext as _

from helpers.models import BaseModel


class Publisher(BaseModel):
    """
    Represents a book publisher in the library.

    Publishers are entities responsible for producing and distributing books.
    This model holds information about different publishers of the books
    available in the library.

    Attributes:
        name (str): The name of the publisher.
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_('Publisher Name'),
        help_text=_('Publisher Name')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Publisher')
        verbose_name_plural = _('Publishers')
        ordering = ['name']
        db_table = 'library_publisher'
