
from django.contrib import admin
from django.urls import path , include
from .views import EquipmentListView, BookingCreateView , ReturnEquipmentView , BookingHistoryView

app_name = 'renting'

urlpatterns = [
    path('equipment/', EquipmentListView.as_view(), name='equipment_list'),
    path('booking/<int:equipment_id>/', BookingCreateView.as_view(), name='booking'),
    path('return/<int:pk>/', ReturnEquipmentView.as_view(), name='return_equipment'),
    path('booking-history/', BookingHistoryView.as_view(), name='booking_history'),
]

