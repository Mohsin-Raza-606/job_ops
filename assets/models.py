from django.db import models


class BaseTimeStamp(models.Model):
    """
    Abstract base model that provides common timestamp and active status fields.

    Fields:
        is_active (bool): Indicates whether the record is active.
        created_at (datetime): Stores the timestamp when the record was created.
        updated_at (datetime): Stores the timestamp when the record was last updated.
    """

    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether this record is active."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when this record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when this record was last updated."
    )

    class Meta:
        abstract = True  # Ensures this model is not created as a table
        ordering = ["-created_at"]  # Default ordering by creation time (latest first)

    def __str__(self):
        """String representation for debugging purposes."""
        return f"{self.__class__.__name__}(id={self.id}, active={self.is_active})"
