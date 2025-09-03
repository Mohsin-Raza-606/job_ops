"""
Models for job and task management.

This module defines models related to jobs, job assignments, and tasks.
It includes support for priorities, statuses, technician assignments,
and equipment relationships.
"""

from django.db import models
from django.utils import timezone
from django.conf import settings

from assets.models import BaseTimeStamp
from equipment.models import Equipment


class Job(BaseTimeStamp):
    """
    Represents a job in the system.

    A job is created by a user, may be assigned to a technician,
    and contains multiple tasks and equipment associations.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    title = models.CharField(
        max_length=200,
        help_text="Title of the job."
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the job."
    )
    client_name = models.CharField(
        max_length=200,
        help_text="Name of the client associated with the job."
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="jobs_created",
        help_text="User who created the job."
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Current status of the job."
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        help_text="Priority level of the job."
    )
    scheduled_date = models.DateField(
        default=timezone.now,
        help_text="Scheduled date for the job."
    )
    is_overdue = models.BooleanField(
        default=False,
        help_text="Indicates whether the job is overdue."
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="jobs_assigned",
        null=True,
        blank=True,
        help_text="Technician or user assigned to the job."
    )

    class Meta:
        ordering = ["-scheduled_date", "-created_at"]

    def __str__(self):
        return self.title


class JobAssignment(BaseTimeStamp):
    """
    Represents the assignment of a technician to a job.

    Each job can have multiple assignments, but each technician
    can only be assigned once per job.
    """

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_assignments"
    )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("job", "technician")
        verbose_name = "Job Assignment"
        verbose_name_plural = "Job Assignments"

    def __str__(self):
        return f"{self.technician} assigned to {self.job}"


class JobTask(BaseTimeStamp):
    """
    Represents an individual task within a job.

    Tasks can be associated with multiple equipment items
    and are tracked separately with their own status and completion time.
    """

    title = models.CharField(
        max_length=200,
        help_text="Title of the task."
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the task."
    )
    status = models.CharField(
        max_length=20,
        choices=Job.Status.choices,
        default=Job.Status.DRAFT,
        help_text="Current status of the task."
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when the task was completed."
    )
    equipments = models.ManyToManyField(
        Equipment,
        related_name="task_assignments",
        blank=True,
        help_text="Equipment associated with this task."
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,  # ⚠️ Kept due to migration issue
        blank=True,
        help_text="The job this task belongs to."
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_user",
        null=True,
        blank=True,
        help_text="User who created the task."
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
