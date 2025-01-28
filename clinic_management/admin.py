from django.contrib import admin
from .models import Doctor, Appointment

from django.contrib import admin
from .models import Doctor, DoctorSchedule, Slot
from django.utils.html import format_html


# Register the Doctor model in the admin
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'mobile_number', 'is_verified', 'created_at')
    search_fields = ('name', 'mobile_number')


# Register the DoctorSchedule model in the admin
@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time')
    search_fields = ('doctor__name', 'day_of_week')
    list_filter = ('doctor', 'day_of_week')


# Register the Slot model in the admin
@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('doctor_schedule', 'start_time', 'end_time', 'is_available')
    search_fields = ('doctor_schedule__doctor__name',)
    list_filter = ('is_available', 'doctor_schedule__day_of_week')

    def doctor_name(self, obj):
        return obj.doctor_schedule.doctor.name

    doctor_name.short_description = 'Doctor Name'
