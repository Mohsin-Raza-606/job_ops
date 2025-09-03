from rest_framework import serializers
from .models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ["id", "name", "type", "serial_number", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]