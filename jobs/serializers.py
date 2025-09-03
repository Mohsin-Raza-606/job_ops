from rest_framework import serializers
from equipment.serializers import ListEquipmentSerializer
from users.serializers import UserSerializer
from .models import Job, JobTask, JobAssignment
from equipment.models import Equipment


class JobTaskSerializer(serializers.ModelSerializer):
    equipments = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = JobTask
        fields = ["id", "title", "description", "status", "completed_at", "equipments", "created_by"]
        read_only_fields = ["completed_at", "created_by"]


class JobSerializer(serializers.ModelSerializer):
    tasks = JobTaskSerializer(many=True, required=False)

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "client_name",
            "status",
            "priority",
            "scheduled_date",
            "is_overdue",
            "tasks",
            "assigned_to",
        ]
        read_only_fields = ["id", "is_overdue"]

    def create(self, validated_data):
        tasks_data = validated_data.pop("tasks", [])
        job = Job.objects.create(**validated_data)

        for task_data in tasks_data:
            equipments = task_data.pop("equipments", [])
            task = JobTask.objects.create(job=job, created_by=self.context["request"].user, **task_data)
            task.equipments.set(equipments)

        return job

    def update(self, instance, validated_data):
        tasks_data = validated_data.pop("tasks", None)

        # update job fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tasks_data is not None:
            existing_tasks = {task.id: task for task in instance.tasks.all()}
            incoming_ids = []

            for task_data in tasks_data:
                equipments = task_data.pop("equipments", [])
                task_id = task_data.get("id")

                if task_id and task_id in existing_tasks:
                    # update existing task
                    task = existing_tasks[task_id]
                    for attr, value in task_data.items():
                        setattr(task, attr, value)
                    task.save()
                    task.equipments.set(equipments)
                    incoming_ids.append(task_id)
                else:
                    # create new task (set created_by explicitly)
                    new_task = JobTask.objects.create(
                        job=instance,
                        created_by=self.context["request"].user,
                        **task_data
                    )
                    new_task.equipments.set(equipments)
                    incoming_ids.append(new_task.id)

            # delete removed tasks
            for task_id, task in existing_tasks.items():
                if task_id not in incoming_ids:
                    task.delete()

        return instance


class ListJobTaskSerializer(serializers.ModelSerializer):
    equipments = ListEquipmentSerializer(many=True)
    created_by = UserSerializer()

    class Meta:
        model = JobTask
        fields = ["id", "title", "description", "status", "completed_at", "equipments", "created_by"]


class ListJobSerializer(serializers.ModelSerializer):
    tasks = ListJobTaskSerializer(many=True)
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "client_name",
            "status",
            "priority",
            "scheduled_date",
            "is_overdue",
            "tasks",
            "created_by",
            "assigned_to",
        ]


class JobAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAssignment
        fields = ["id", "job", "technician"]
        read_only_fields = ["id"]

    def validate(self, data):
        job = data["job"]

        if job.status in [Job.Status.COMPLETED, Job.Status.CANCELED]:
            raise serializers.ValidationError("Cannot assign a completed or canceled job.")

        if data["technician"].role != "technician":
            raise serializers.ValidationError("Assigned user must have technician role.")

        return data

    def create(self, validated_data):
        job = validated_data["job"]
        technician = validated_data["technician"]

        # Deactivate old assignments
        JobAssignment.objects.filter(job=job).update(is_active=False)

        # Create new assignment
        assignment = JobAssignment.objects.create(**validated_data, is_active=True)

        # Update the Job.assigned_to field
        job.assigned_to = technician
        job.save(update_fields=["assigned_to"])

        return assignment


class ListJobAssignmentSerializer(serializers.ModelSerializer):
    technician = UserSerializer()

    class Meta:
        model = JobAssignment
        fields = ["job", "technician", "id"]
