from django.urls import path
from .views import TechnicianDashboardView

urlpatterns = [
    path("technician/", TechnicianDashboardView.as_view(), name="technician-dashboard"),
]
