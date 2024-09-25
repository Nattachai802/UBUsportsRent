from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin , LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.messages.views import SuccessMessageMixin


from base.models import *
from management_equipment.form import Equipment
# Create your views here.


#CRUD - Read 
class Viewequipment(LoginRequiredMixin , UserPassesTestMixin , ListView):
    model  = Equipment
    template_name = 'equipment_list.html'
    context_object_name = 'equipment'

    def test_func(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return True

#CRUD - Create
class EquipmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView,SuccessMessageMixin):
    model = Equipment
    fields = ['name', 'type', 'available_amount', 'picture']
    template_name = 'equipment_form.html'
    success_url = reverse_lazy('Manageq:View')
    success_message = "Equipment successfully created."

    def test_func(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return True

#CRUD - Update
class EquipmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView,SuccessMessageMixin):
    model = Equipment
    fields = ['name', 'type', 'available_amount', 'picture_url']
    template_name = 'equipment_form.html'
    success_url = reverse_lazy('Manageq:View')
    success_message = "Equipment successfully updated."

    def test_func(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return True
#CRUD - Delete
class EquipmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView,SuccessMessageMixin):
    model = Equipment
    template_name = 'equipment_confirm_delete.html'
    success_url = reverse_lazy('Manageq:View')
    success_message = "Equipment successfully deleted."

    def test_func(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return True