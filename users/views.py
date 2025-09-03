from rest_framework import viewsets
from users.permissions import IsAdmin
from .serializers import UserSerializer, AdminCreateUserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == "create":
            return AdminCreateUserSerializer
        return UserSerializer

    def perform_create(self, serializer):
        """Ensure created_by or any extra logic if needed later."""
        serializer.save()

