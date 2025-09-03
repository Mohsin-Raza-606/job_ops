"""
Custom permission classes for user roles and job/task restrictions.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS

from jobs.models import JobAssignment


class IsAdmin(BasePermission):
    """
    Allow access only to users with the "admin" role.
    """

    def has_permission(self, request, view):
        return (
                request.user
                and request.user.is_authenticated
                and request.user.role == "admin"
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Allow read-only access for everyone,
    but restrict write access to users with the "admin" role.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
                request.user
                and request.user.is_authenticated
                and request.user.role == "admin"
        )


class IsAdminOrSalesAgent(BasePermission):
    """
    Allow access only to users with "admin" or "sales_agent" roles.
    """

    def has_permission(self, request, view):
        return (
                request.user
                and request.user.is_authenticated
                and request.user.role in ["admin", "sales_agent"]
        )


class IsLastActiveTechnician(BasePermission):
    """
    Allows only the technician assigned to a job
    to add/edit/delete its tasks.
    Admins always allowed.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admins can do anything
        if user.role == "admin":
            return True

        # Figure out which job this task belongs to
        job = getattr(obj, "job", None)
        if job is None:
            return False

        # Check if the current user is the assigned technician
        return job.assigned_to_id == user.id
