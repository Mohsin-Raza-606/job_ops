"""
Dashboard views for technicians.

This module provides APIs related to technician dashboards,
including retrieving assigned job tasks grouped by scheduled date.
"""

from collections import defaultdict
from datetime import date, datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from jobs.models import JobTask, Job


class TechnicianDashboardView(APIView):
    """
    API endpoint for technicians to view their assigned job tasks.

    Returns a list of tasks grouped by job scheduled date.
    Supports optional filtering by date range.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests to fetch technician dashboard data.

        Query Params:
            from_date (str, optional): Start date filter (format: YYYY-MM-DD).
            to_date   (str, optional): End date filter (format: YYYY-MM-DD).

        Response:
            200 OK: List of job tasks grouped by scheduled date.
            400 Bad Request: If invalid date format is provided.
            403 Forbidden: If the user is not a technician (optional check).
        """
        user = request.user

        # 🔒 Restrict access to technicians only (uncomment if roles exist)
        if not hasattr(user, "role") or user.role != "technician":
            return Response(
                {"detail": "Only technicians can access this endpoint."},
                status=403,
            )

        # Extract optional query params
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        # Validate date params
        try:
            if from_date:
                from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            if to_date:
                to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"detail": "Invalid date format. Use YYYY-MM-DD."},
                status=400,
            )

        # Base queryset → tasks from jobs assigned to this technician
        tasks = (
            JobTask.objects
            .select_related("job")
            .prefetch_related("equipments")  # avoids N+1 queries
            .filter(
                job__assigned_to=user,
                status__in=[Job.Status.SCHEDULED, Job.Status.IN_PROGRESS],
            )
            .order_by("job__scheduled_date", "id")
        )

        # Apply date filters if provided
        if from_date:
            tasks = tasks.filter(job__scheduled_date__gte=from_date)
        if to_date:
            tasks = tasks.filter(job__scheduled_date__lte=to_date)

        # Group tasks by job scheduled date
        grouped_tasks = defaultdict(list)
        for task in tasks:
            task_date = task.job.scheduled_date or date.today()
            grouped_tasks[task_date].append({
                "job_id": task.job.id,
                "job_title": task.job.title,
                "task_id": task.id,
                "task_title": task.title,
                "task_status": task.status,
                "equipments": [
                    {
                        "id": equipment.id,
                        "name": equipment.name,
                        "serial_number": equipment.serial_number,
                    }
                    for equipment in task.equipments.all()
                ],
            })

        # Format response: sorted by date
        response_data = [
            {"date": d.isoformat(), "tasks": items}
            for d, items in sorted(grouped_tasks.items(), key=lambda x: x[0])
        ]

        return Response(response_data)
