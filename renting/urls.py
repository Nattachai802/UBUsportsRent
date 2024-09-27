
from django.contrib import admin
from django.urls import path , include
from .views import EquipmentListView, BookingCreateView , ReturnEquipmentView , BookingHistoryView , MyRentalsView

app_name = 'renting'

urlpatterns = [
    path('equipment/', EquipmentListView.as_view(), name='equipment_list'),
    path('booking/<int:equipment_id>/', BookingCreateView.as_view(), name='booking'),
    
    path('my-rentals/', MyRentalsView.as_view(), name='my_rentals'),
    path('return/<int:booking_id>/', ReturnEquipmentView.as_view(), name='return_equipment'),
    
    path('booking-history/', BookingHistoryView.as_view(), name='booking_history'),
]

