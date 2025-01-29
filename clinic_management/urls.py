# clinic_management/urls.py
from django.urls import path
from .views import SlotListView, BookAppointmentView, GetAppointmentsView

urlpatterns = [
    # path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<uuid:doctor_id>/slots/', SlotListView.as_view(), name='doctor-slots-list'),
    path('appointments/book/<str:slot_id>/', BookAppointmentView.as_view(), name='book-appointment'),
    path('appointments/', GetAppointmentsView.as_view(), name='get-appointments'),
]