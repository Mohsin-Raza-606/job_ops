from django.conf import settings
from django.db import models
from assets.models import BaseTimeStamp


class Equipment(BaseTimeStamp):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=80)
    serial_number = models.CharField(max_length=120, unique=True)
    crated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="equipment_crated_by")


    class Meta:
        indexes = [models.Index(fields=["serial_number"])]
        ordering = ["name"]


    def __str__(self):
        return f"{self.name} ({self.serial_number})"