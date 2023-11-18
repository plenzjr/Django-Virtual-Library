from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator

from helpers.models import BaseModel


class BookReview(BaseModel):
    """
    Model representing a review of a book.

    Attributes:
        user (ForeignKey): The user who wrote the review.
        book (ForeignKey): The book that the review is about.
        review (TextField): The content of the review.
        rating (PositiveSmallIntegerField): A numerical rating given to the book by the user.
    """

    user = models.ForeignKey(
        'app_account.User',
        on_delete=models.CASCADE,
        db_column='user_uid',
        verbose_name=_('User'),
        help_text=_('User who wrote the review'),
        related_name='book_reviews'
    )
    book = models.ForeignKey(
        'app_library.Book',
        on_delete=models.CASCADE,
        db_column='book_uid',
        verbose_name=_('Book'),
        help_text=_('Book being reviewed'),
        related_name='reviews'
    )
    review = models.TextField(
        verbose_name=_('Review'),
        help_text=_('Content of the review')
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name=_('Rating'),
        help_text=_('Numerical rating of the book'),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.user.full_name}'s review of {self.book.title}"

    class Meta:
        verbose_name = _('Book Review')
        verbose_name_plural = _('Book Reviews')
        ordering = ['-rating', 'created_at']
        db_table = 'library_book_review'
