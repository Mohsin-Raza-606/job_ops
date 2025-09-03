"""
Views for equipment management.

This module defines a ViewSet for managing equipment, including
listing, creating, updating, searching, and activating/deactivating equipment.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from users.permissions import IsAdminOrReadOnly
from .serializers import EquipmentSerializer
from .models import Equipment


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing equipment records.

    Features:
        - Admins can create, update, and toggle equipment activation.
        - Read-only access for other users.
        - Supports filtering by `is_active` and searching by name, type, or serial number.
    """

    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    # Filtering and searching support
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["is_active"]
    search_fields = ["name", "type", "serial_number"]

    def perform_create(self, serializer):
        """
        Automatically assign the currently authenticated user as the creator.
        """
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to implement soft-delete behavior.

        Instead of deleting an equipment record, toggle its `is_active` status.
        """
        instance = self.get_object()
        if instance.is_active:
            instance.is_active = False
            action = "deactivated"
        else:
            instance.is_active = True
            action = "activated"

        instance.save(update_fields=["is_active"])

        return Response(
            {"detail": f"Equipment successfully {action}."},
            status=status.HTTP_200_OK,
        )
