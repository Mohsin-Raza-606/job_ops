"""
Models for equipment management.

This module defines the Equipment model, which represents
a physical asset tracked in the system.
"""

from django.conf import settings
from django.db import models
from assets.models import BaseTimeStamp


class Equipment(BaseTimeStamp):
    """
    Represents a piece of equipment in the system.

    Inherits common timestamp and active fields from BaseTimeStamp.

    Fields:
        name (str): Human-readable name of the equipment.
        type (str): Category or type of equipment (e.g., "Generator").
        serial_number (str): Unique identifier for the equipment.
        created_by (User): User who created the record.
    """

    name = models.CharField(
        max_length=120,
        help_text="Name of the equipment (e.g., Air Compressor)."
    )
    type = models.CharField(
        max_length=80,
        help_text="Category/type of the equipment (e.g., Electrical, Mechanical)."
    )
    serial_number = models.CharField(
        max_length=120,
        unique=True,
        help_text="Unique serial number of the equipment."
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="equipment_created_by",  # ✅ fixed typo
        help_text="The user who created this equipment record."
    )

    class Meta:
        indexes = [
            models.Index(fields=["serial_number"]),
        ]
        ordering = ["name"]
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"

    def __str__(self):
        """Return a human-readable string representation of the equipment."""
        return f"{self.name} ({self.serial_number})"
