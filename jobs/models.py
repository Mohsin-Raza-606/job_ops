# from django.db import models
# from django.utils import timezone
# from django.conf import settings
# from assets.models import BaseTimeStamp
# from equipment.models import Equipment
#
#
# class Job(BaseTimeStamp):
#     class Status(models.TextChoices):
#         DRAFT = "draft", "Draft"
#         SCHEDULED = "scheduled", "Scheduled"
#         IN_PROGRESS = "in_progress", "In Progress"
#         COMPLETED = "completed", "Completed"
#         CANCELED = "canceled", "Canceled"
#
#
#     class Priority(models.TextChoices):
#         LOW = "low", "Low"
#         MEDIUM = "medium", "Medium"
#         HIGH = "high", "High"
#         URGENT = "urgent", "Urgent"
#
#
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     client_name = models.CharField(max_length=200)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="jobs_created")
#     status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
#     priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
#     scheduled_date = models.DateField(default=timezone.now)
#     is_overdue = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.title
#
#
# class Assignment(BaseTimeStamp):
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="assignments")
#     technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignments")
#
#     class Meta:
#         unique_together = ("job", "technician")
#
#     def __str__(self):
#         return f"{self.technician} assigned to {self.job}"
#
# class JobTask(BaseTimeStamp):
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     status = models.CharField(max_length=20, choices=Job.Status.choices, default=Job.Status.DRAFT)
#     completed_at = models.DateTimeField(null=True, blank=True)
#     equipments = models.ManyToManyField(Equipment, related_name="assignments", blank=True)
#
#
#     def __str__(self):
#         return self.title