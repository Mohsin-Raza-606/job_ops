from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        TECHNICIAN = "technician", "Technician"
        SALES_AGENT = "sales_agent", "Sales Agent"


    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.TECHNICIAN)


    @property
    def is_admin(self) -> bool:
        return self.role == self.Roles.ADMIN