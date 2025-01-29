# clinic_management/serializers.py
from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import Doctor, Appointment, Slot


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'age', 'gender', 'mobile_number', 'photo_url', 'is_verified',
                  'created_at']


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'start_time', 'end_time', 'is_available']


# Main Appointment Serializer
class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer()  # Nested UserSerializer for patient details
    doctor = DoctorSerializer()  # Nested DoctorSerializer for doctor details
    slot = SlotSerializer()  # Nested SlotSerializer for slot details

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'slot', 'status']  # Include other fields as necessary
