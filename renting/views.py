from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic import CreateView, ListView , UpdateView
from base.models import Booking
from .forms import BookingForm , ReturnForm


class EquipmentListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'renting/equipment_list.html'
    context_object_name = 'equipments'

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'renting/booking_form.html'
    success_url = reverse_lazy('renting:equipment_list')

    def form_valid(self, form):
        equipment = form.cleaned_data['equipment']
        if equipment.available_amount <= 0:
            form.add_error('equipment', 'อุปกรณ์นี้ไม่มีให้เช่าในขณะนี้')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReturnEquipmentView(UpdateView):
    model = Booking
    form_class = ReturnForm
    template_name = 'renting/return_form.html'
    success_url = reverse_lazy('renting:equipment_list')

    def form_valid(self, form):
        form.instance.return_date = form.cleaned_data['return_date']
        form.instance.equipment.available_amount += form.instance.amount  # Increase available amount
        form.instance.equipment.save()
        
        return super().form_valid(form)
    

class BookingHistoryView(ListView):
    model = Booking
    template_name = 'renting/booking_history.html'
    context_object_name = 'bookings'
    paginate_by = 10  # Optional: paginate the list if there are many bookings

    def get_queryset(self):
        # Filter bookings by the logged-in user
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')