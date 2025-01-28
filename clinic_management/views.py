from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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


# Create the API view for fetching the list of doctors
@api_view(['GET'])
@permission_classes([AllowAny])
class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    pagination_class = ListPagination
    # permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([AllowAny])
class SlotListView(generics.ListAPIView):
    serializer_class = SlotSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        doctor_schedule = DoctorSchedule.objects.filter(doctor_id=doctor_id)

        if not doctor_schedule.exists():
            return Slot.objects.none()  # Return empty queryset if no schedule found

        slots = Slot.objects.filter(doctor_schedule__in=doctor_schedule, is_available=True)

        return slots

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ScheduleAppointmentView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
