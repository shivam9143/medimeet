"""
URL configuration for medimeet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from authentication.views import RegisterUserAPIView, VerifyOTPAPIView, SendOtpAPIView
from clinic_management.views import DoctorListView, ScheduleAppointmentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register-user/', RegisterUserAPIView.as_view(), name="register-user"),
    path('send-otp/', SendOtpAPIView.as_view(), name="send-otp"),
    path("verify-otp/", VerifyOTPAPIView.as_view(), name="verify-user"),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('appointments/', ScheduleAppointmentView.as_view(), name='schedule-appointment'),
]
