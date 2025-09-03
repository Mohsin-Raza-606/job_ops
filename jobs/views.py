# jobs/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from django.db.models import Prefetch
from rest_framework.response import Response
from users.permissions import IsAdminOrSalesAgent, IsLastActiveTechnician
from .models import Job, JobTask, JobAssignment
from .serializers import (
    JobSerializer,
    ListJobSerializer,
    JobTaskSerializer,
    ListJobTaskSerializer,
    JobAssignmentSerializer,
    ListJobAssignmentSerializer,
)


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter(is_active=True).select_related(
        "created_by", "assigned_to"
    ).prefetch_related(
        Prefetch(
            "tasks",
            queryset=JobTask.objects.filter(is_active=True)
            .select_related("created_by")
            .prefetch_related("equipments"),
        )
    )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "priority", "is_overdue", "is_active"]
    search_fields = ["title"]
    permission_classes = [IsAdminOrSalesAgent]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ListJobSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_active:
            instance.is_active = False
            action = "deactivated"
        else:
            instance.is_active = True
            action = "activated"
        instance.save()
        return Response(
            {"detail": f"Job successfully {action}."}, status=status.HTTP_200_OK
        )


class JobAssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = JobAssignmentSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter(is_active=True).select_related("job", "technician")
    permission_classes = [IsAdminOrSalesAgent]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["job", "technician", "is_active"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ListJobAssignmentSerializer
        return self.serializer_class

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_active:
            instance.is_active = False
            action = "deactivated"
        else:
            instance.is_active = True
            action = "activated"
        instance.save()
        return Response(
            {"detail": f"Job assignment successfully {action}."},
            status=status.HTTP_200_OK,
        )


class JobTaskViewSet(viewsets.ModelViewSet):
    serializer_class = JobTaskSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter(is_active=True).select_related(
        "job", "created_by"
    ).prefetch_related("equipments")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "is_active"]
    search_fields = ["title", "description"]
    permission_classes = [IsLastActiveTechnician]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ListJobTaskSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        """
        Support bulk create (list of tasks) or single task create.
        """
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)

        if many:
            tasks = []
            for task_data in serializer.validated_data:
                task = JobTask.objects.create(created_by=request.user, **task_data)
                tasks.append(task)
                self._update_job_status(task.job)
        else:
            task = serializer.save(created_by=request.user)
            self._update_job_status(task.job)
            tasks = task

        return Response(
            self.get_serializer(tasks, many=many).data,
            status=status.HTTP_201_CREATED,
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        self._update_job_status(instance.job)

    def perform_destroy(self, instance):
        job = instance.job
        instance.delete()
        if job:
            self._update_job_status(job)

    def _update_job_status(self, job: Job):
        """Automatically update job status depending on tasks."""
        if not job:
            return

        tasks = job.tasks.filter(is_active=True)
        if tasks.exists():
            if all(t.status == Job.Status.COMPLETED for t in tasks):
                job.status = Job.Status.COMPLETED
            else:
                if job.status not in [Job.Status.CANCELED, Job.Status.DRAFT]:
                    job.status = Job.Status.IN_PROGRESS
        else:
            # If no active tasks remain, reset to draft (business rule)
            job.status = Job.Status.DRAFT
        job.save(update_fields=["status"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_active:
            instance.is_active = False
            action = "deactivated"
        else:
            instance.is_active = True
            action = "activated"
        instance.save()

        self._update_job_status(instance.job)
        return Response(
            {"detail": f"Job task successfully {action}."}, status=status.HTTP_200_OK
        )
