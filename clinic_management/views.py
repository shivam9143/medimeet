import traceback

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CustomJWTAuthentication import CustomJWTAuthentication
from core.create_response import create_response
from .models import Appointment, DoctorSchedule, Slot
from .models import Doctor
from .serializers import AppointmentSerializer, SlotSerializer
from .serializers import DoctorSerializer


class DoctorListAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        try:
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

        except APIException as e:
            error_trace = traceback.format_exc()  # Get full traceback
            # logger.error(f"Error during OTP verification: {e}")
            return create_response(
                code=status.HTTP_400_BAD_REQUEST,
                message="An error occurred while fetching doctors.",
                error=f"{str(e)} | Traceback: {error_trace}"  # Include traceback in response (optional)
            )
        except Exception as e:
            error_trace = traceback.format_exc()  # Get full traceback
            # Catch any other unexpected exceptions
            return create_response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An unexpected error occurred.",
                error=f"{str(e)} | Traceback: {error_trace}",  # Include traceback in response (optional)
                data=None
            )


class SlotListView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookAppointmentView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the slot_id from URL parameters
        slot_id = kwargs.get('slot_id')

        if not slot_id:
            return create_response(status.HTTP_400_BAD_REQUEST, error="Slot ID missing", message="Slot ID is required.")

        # Attempt to retrieve the slot
        try:
            slot = Slot.objects.get(id=slot_id)
        except Slot.DoesNotExist:
            return create_response(status.HTTP_404_NOT_FOUND, error="Slot not found",
                                   message="The requested slot does not exist.")

        # Check if the slot is available
        if not slot.is_available:
            return create_response(status.HTTP_400_BAD_REQUEST, error="Slot not available",
                                   message="The requested slot is already booked.")

        # Attempt to create the appointment
        try:
            # Create the appointment
            appointment = Appointment.objects.create(
                patient=request.user,  # Assuming the user is authenticated
                slot=slot,
                doctor=slot.doctor_schedule.doctor,
                status='Booked'
            )

            # Mark the slot as unavailable
            slot_serializer = SlotSerializer(slot, data={"is_available": False}, partial=True)
            if slot_serializer.is_valid():
                slot_serializer.save()

            # Return the appointment details
            return create_response(status.HTTP_201_CREATED, data={
                "id": appointment.id,
                "patient": appointment.patient.id,
                "doctor": appointment.doctor.id,
                "appointment_time": str(slot),
                "status": appointment.status
            }, message="Appointment successfully booked.")

        except Exception as e:
            # Return error in case of any failure during appointment creation
            return create_response(status.HTTP_400_BAD_REQUEST, error=str(e), message="Something went wrong!")


class GetAppointmentsView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch appointments only for the authenticated user
        try:
            appointments = Appointment.objects.filter(patient=request.user)

            if not appointments:
                return create_response(status.HTTP_404_NOT_FOUND, error="No appointments found",
                                       message="You have no appointments.")

            # Serialize the appointments
            serializer = AppointmentSerializer(appointments, many=True)

            return create_response(status.HTTP_200_OK, data=serializer.data,
                                   message="Appointments retrieved successfully.")

        except Exception as e:
            return create_response(status.HTTP_400_BAD_REQUEST, error=str(e), message="Something went wrong!")


class CancelAppointmentView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        slot_id = request.data.get("slot_id")

        if not slot_id:
            return create_response(message="Slot ID is required.", code=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the appointment for this user and slot
            appointment = Appointment.objects.filter(slot_id=slot_id, patient=request.user).latest('id')

            # Mark the slot as available
            slot = appointment.slot
            slot.is_available = True
            slot.save()

            # Update appointment status to 'Cancelled' instead of deleting it
            appointment.status = "Cancelled"
            appointment.save()

            return create_response(
                message="Appointment cancelled successfully.",
                code=status.HTTP_200_OK
            )

        except Appointment.DoesNotExist:
            return create_response(
                message="No appointment found for this slot.",
                code=status.HTTP_404_NOT_FOUND
            )
