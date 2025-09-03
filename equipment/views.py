from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from users.permissions import IsAdminOrReadOnly
from .serializers import EquipmentSerializer


class EquipmentViewSet(viewsets.ModelViewSet):

    serializer_class = EquipmentSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_deleted']
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
