"""
Package initializer for the Django project.

This file ensures that the Celery application is always imported
when Django starts, so that shared tasks will be recognized and
executed properly.
"""

from .celery import app as celery_app

# Expose Celery app instance when "from project import *" is used
__all__ = ("celery_app",)
