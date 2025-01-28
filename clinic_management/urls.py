# clinic_management/urls.py
from django.urls import path
from .views import  SlotListView

urlpatterns = [
    # path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<uuid:doctor_id>/slots/', SlotListView.as_view(), name='doctor-slots-list'),
    path('doctors/<uuid:doctor_id>/slots/', SlotListView.as_view(), name='doctor-slots-list'),
]