from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic import CreateView, ListView , UpdateView , FormView
from base.models import Booking , Equipment
from .forms import BookingForm , ReturnForm


class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = 'renting/equipment_list.html'
    context_object_name = 'equipments'



class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'renting/booking_form.html'
    success_url = reverse_lazy('renting:equipment_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment'] = Equipment.objects.get(id=self.kwargs['equipment_id'])
        return context

    def form_valid(self, form):
        # Get the equipment object
        equipment = Equipment.objects.get(id=self.kwargs['equipment_id'])
        requested_amount = form.cleaned_data['amount']
        
        # Check if there are enough items available
        if equipment.available_amount < requested_amount:
            form.add_error('amount', f'อุปกรณ์นี้มีเหลือเพียง {equipment.available_amount} หน่วยเท่านั้น')
            return self.form_invalid(form)
        
        # Update equipment available amount
        equipment.available_amount -= requested_amount
        equipment.save()
        
        # Set the user and equipment fields in the booking instance
        form.instance.user = self.request.user
        form.instance.equipment = equipment
        
        # Set booking status to pending
        form.instance.status = 'Pending' 
        
        return super().form_valid(form)

class MyRentalsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'renting/my_rentals.html'
    context_object_name = 'current_rentals'

    def get_queryset(self):
        # Filter bookings that belong to the user and have 'Rented' status
        return Booking.objects.filter(user=self.request.user, status='Rented')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add rental history (returned items) to the context
        context['current_rentals'] = Booking.objects.filter(user=self.request.user, status='approved')
        context['rental_history'] = Booking.objects.filter(user=self.request.user, status='Returned')
        return context

class ReturnEquipmentView(LoginRequiredMixin, FormView):
    template_name = 'renting/return_confirm.html'
    success_url = reverse_lazy('renting:my_rentals')

    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, id=self.kwargs['booking_id'], user=request.user)
        equipment = booking.equipment

        # Mark the booking as 'Returned'
        booking.status = 'Returned'
        booking.save()

        # Update the available amount in Equipment
        equipment.available_amount += booking.amount
        equipment.save()

        return redirect(self.success_url)
    

class BookingHistoryView(ListView):
    model = Booking
    template_name = 'renting/booking_history.html'
    context_object_name = 'bookings'
    paginate_by = 10  # Optional: paginate the list if there are many bookings

    def get_queryset(self):
        # Filter bookings by the logged-in user
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')