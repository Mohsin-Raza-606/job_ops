from rest_framework import viewsets
from users.permissions import IsAdmin
from .serializers import UserSerializer, AdminCreateUserSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all().order_by("id")
    permission_classes = [IsAdmin]


    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AdminCreateUserSerializer
        return self.serializer_class
