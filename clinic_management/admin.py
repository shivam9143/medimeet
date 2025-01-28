from django.contrib import admin
from .models import Doctor, Appointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'specialization', 'available_slots', 'gender', 'mobile_number', 'is_verified', 'created_at')
    search_fields = ('name', 'mobile_number', 'specialization')
    list_filter = ('is_verified', 'gender', 'created_at')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'time_slot', 'status')
    search_fields = ('patient__name', 'doctor__name', 'status')
    list_filter = ('status', 'time_slot', 'doctor', 'patient')
    list_editable = ('status',)  # Make the 'status' field editable directly from the list view