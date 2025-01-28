import uuid

from django.db import models

from authentication.models import User


class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    available_slots = models.JSONField()  # Example: ["2025-01-28T10:00", "2025-01-28T11:00"]
    age = models.PositiveIntegerField(null=False)
    gender = models.CharField(max_length=10, null=True, blank=False)
    mobile_number = models.CharField(max_length=15, null=False)
    photo_url = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [("Scheduled", "Scheduled"), ("Canceled", "Canceled")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time_slot = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled")

    def __str__(self):
        return f"{self.patient.name}__{self.doctor.name}"
