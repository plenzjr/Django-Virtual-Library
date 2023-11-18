from django.db import models
from django.utils.translation import gettext as _

from helpers.models import BaseModel


class Category(BaseModel):
    """
    Represents a category for books in the library.

    Categories are used to organize books into various sections, making it
    easier for users to find books of a particular genre or topic.

    Attributes:
        name (str): The name of the category, which should be a short, descriptive label.
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_('Category Name'),
        help_text=_('Category Name')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']
        db_table = 'library_category'
