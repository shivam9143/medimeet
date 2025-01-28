import uuid

from django.db import models

from authentication.models import User

from django.db import models
import uuid


class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, null=True, blank=True)
    mobile_number = models.CharField(max_length=15)
    photo_url = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='schedules', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=9, choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.name}'s Schedule for {self.day_of_week.capitalize()}"

    # You can add additional methods to check availability or generate time slots


class Appointment(models.Model):
    STATUS_CHOICES = [("Scheduled", "Scheduled"), ("Canceled", "Canceled")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time_slot = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled")

    def __str__(self):
        return f"{self.patient.name}__{self.doctor.name}"


class Slot(models.Model):
    doctor_schedule = models.ForeignKey(DoctorSchedule, related_name='slots', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Slot from {self.start_time} to {self.end_time} for {self.doctor_schedule.doctor.name}"
