# clinic_management/serializers.py
from rest_framework import serializers
from .models import Doctor, Appointment, Slot


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'age', 'gender', 'mobile_number', 'photo_url', 'is_verified',
                  'created_at']


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['start_time', 'end_time', 'is_available']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
