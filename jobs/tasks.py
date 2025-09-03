from celery import shared_task
from django.utils import timezone
from .models import Job


@shared_task
def update_overdue_jobs():
    today = timezone.now().date()

    # Mark jobs overdue if they have any task scheduled before today & not completed
    overdue_jobs = Job.objects.filter(
        tasks__status__in=[Job.Status.DRAFT, Job.Status.SCHEDULED, Job.Status.IN_PROGRESS],
        scheduled_date__lt=today,
    ).distinct()

    # Reset all jobs first
    Job.objects.update(is_overdue=False)

    # Mark the overdue ones
    overdue_jobs.update(is_overdue=True)

    return f"{overdue_jobs.count()} jobs marked as overdue."
