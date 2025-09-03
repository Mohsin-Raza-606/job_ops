from django.contrib import admin

from jobs.models import Job, JobTask, JobAssignment

# Register your models here.

admin.site.register(Job)
admin.site.register(JobTask)
admin.site.register(JobAssignment)
