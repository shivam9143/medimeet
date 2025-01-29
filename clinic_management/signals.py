from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DoctorSchedule, Slot
from datetime import datetime, timedelta


# @receiver(post_save, sender=DoctorSchedule)
# def create_slots_for_new_schedule(sender, instance, created, **kwargs):
#     print("runnung ------------")
#     if created:  # Only trigger this when a new schedule is created
#         create_slots_for_schedule(instance)


def create_slots_for_schedule(doctor_schedule):
    start_time = doctor_schedule.start_time
    end_time = doctor_schedule.end_time

    # Convert times to datetime objects for calculation
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)

    # Create slots for 30-minute intervals
    slots = []
    current_time = start_datetime
    while current_time < end_datetime:
        slot_end_time = current_time + timedelta(minutes=30)
        slots.append(Slot(
            doctor_schedule=doctor_schedule,
            start_time=current_time,
            end_time=slot_end_time,
            is_available=True
        ))
        current_time = slot_end_time

    # Bulk create the slots in the database for performance
    Slot.objects.bulk_create(slots)
