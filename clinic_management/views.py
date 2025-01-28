from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Doctor, Appointment
from .serializers import DoctorSerializer, AppointmentSerializer


class DoctorListView(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)


class ScheduleAppointmentView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
