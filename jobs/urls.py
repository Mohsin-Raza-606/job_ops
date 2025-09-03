from rest_framework.routers import DefaultRouter
from .views import JobViewSet, JobAssignmentViewSet, JobTaskViewSet

router = DefaultRouter()
router.register(r"task", JobTaskViewSet, basename="job-task")
router.register(r"assignment", JobAssignmentViewSet, basename="job-assignment")
router.register(r"", JobViewSet, basename="job")

urlpatterns = router.urls
