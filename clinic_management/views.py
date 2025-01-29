import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.create_response import create_response
from .models import User, Doctor, Appointment, DoctorSchedule, Slot
from .serializers import DoctorSerializer, AppointmentSerializer, SlotSerializer

# clinic_management/views.py
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Doctor
from .serializers import DoctorSerializer


# Create a custom pagination class
class ListPagination(PageNumberPagination):
    page_size = 10  # Adjust the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class DoctorListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.all()

        if not doctors.exists():
            # Return 404 with a custom message
            msg = "Doctors not found"
            return create_response(
                code=status.HTTP_404_NOT_FOUND,
                message=msg,
                error=msg,
                data=None
            )

        # Serialize the data
        serializer = DoctorSerializer(doctors, many=True)
        return create_response(
            code=status.HTTP_200_OK,
            message="Doctors retrieved successfully",
            error=None,
            data=serializer.data
        )


class SlotListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, doctor_id, *args, **kwargs):
        # Get the doctor schedule for the given doctor_id
        doctor_schedule = DoctorSchedule.objects.filter(doctor_id=doctor_id)

        # Check if any schedule exists for the doctor, if not return empty response
        if not doctor_schedule.exists():
            return Response([], status=status.HTTP_200_OK)

        # Filter the slots related to the doctor and only available slots
        slots = Slot.objects.filter(doctor_schedule__in=doctor_schedule, is_available=True)

        # Serialize the data
        serializer = SlotSerializer(slots, many=True)

        # Return the response with serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScheduleAppointmentView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookAppointmentView(APIView):

    def post(self, request, *args, **kwargs):
        # Get the request body data (assuming it's JSON)
        slot_id = kwargs.get('slot_id')
        print(f"slot id {slot_id}")
        print("heree 001")

    # Check if the slot exists and is available
        try:
            slot = Slot.objects.get(id=slot_id)
            print(f"Slot availability: {slot.is_available}")

            print("heree 002")
            if not slot.is_available:
                print("heree 003")
                create_response(status.HTTP_400_BAD_REQUEST, error="Slot is not available",
                                message="Something went wrong")
        except Slot.DoesNotExist:
            print("heree 004")
            create_response(status.HTTP_404_NOT_FOUND, error="Slot not found.", message="Something went wrong")
            print("heree 00")

        try:
            # Create the appointment record
            appointment = Appointment.objects.create(
                patient=request.user,  # The user making the request (ensure they are authenticated)
                slot=slot,
                doctor=slot.doctor_schedule.doctor,
                status='Booked'
            )

            print("heree 11")
            serializer = SlotSerializer(slot, data={"is_available": False}, partial=True)
            if serializer.is_valid():
                serializer.save()
            # Mark the slot as booked
            # slot.is_available = False
            # slot.save()
            # print(f"Slot saved? {serializer.is_available}")  # Debugging
            # print("heree 33")

            # Return the appointment details as the response
            return create_response(code=status.HTTP_201_CREATED, data={
                "id": appointment.id,
                "patient": appointment.patient.id,
                "doctor": appointment.doctor.id,
                "appointment_time": str(slot),
                "status": appointment.status
            }, message="Success")
            print("heree 44")

        except Exception as e:
            return create_response(code=status.HTTP_400_BAD_REQUEST, error=str(e), message="Something went wrong!")
