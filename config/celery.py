"""
Celery application configuration for the Django project.

This file initializes and configures the Celery app to work with Django.
It sets the default Django settings module, loads Celery settings from
Django's settings file (with the CELERY_ prefix), and auto-discovers tasks
from all registered Django apps.
"""

import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Create Celery app instance
app = Celery("config")  # Use your project name (replace 'config' if different)

# Load configuration from Django settings, using CELERY_ namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed Django apps
app.autodiscover_tasks()


