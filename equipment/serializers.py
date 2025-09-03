"""
Serializers for the Equipment model.

This module defines serializers for creating, updating, and listing equipment.
"""

from rest_framework import serializers
from .models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating equipment records.

    Includes all relevant fields, with `id`, `created_at`, and `updated_at`
    marked as read-only since they are automatically managed.
    """

    class Meta:
        model = Equipment
        fields = [
            "id",
            "name",
            "type",
            "serial_number",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ListEquipmentSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing equipment records.

    Only includes the most essential fields.
    """

    class Meta:
        model = Equipment
        fields = ["id", "name", "type", "serial_number"]
