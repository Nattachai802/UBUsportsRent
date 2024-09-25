from django.urls import path , include
from management_equipment.views import *
from django.contrib.auth import views as auth_views
app_name = 'Manageq'

urlpatterns = [
    path('equip/', Viewequipment.as_view(), name='View'),
    path('equip/new/', EquipmentCreateView.as_view(), name='equipment_create'),
    path('equip/<int:pk>/edit/', EquipmentUpdateView.as_view(), name='equipment_update'),
    path('equip/<int:pk>/delete/', EquipmentDeleteView.as_view(), name='equipment_delete'),
]