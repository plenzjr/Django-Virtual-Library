import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model class for adding timestamp fields.

    This class provides two fields: `created_at` and `updated_at` which are
    automatically set to the current date and time when the object is created
    and updated, respectively.

    Fields:
        - uid (UUIDField): Field to store the unique identifier.
        - created_at (DateTimeField): Field to store the creation timestamp.
        - updated_at (DateTimeField): Field to store the last update timestamp.
    """

    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(
        blank=True,
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        blank=True,
        auto_now=True
    )

    class Meta:
        abstract = True
