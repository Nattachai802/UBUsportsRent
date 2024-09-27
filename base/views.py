from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.contrib.auth.views import LoginView , PasswordResetView
from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model

from base.models import *
from base.form import UserRegisterForms
# Create your views here.

class UserRegisterview(CreateView):
    form_class = UserRegisterForms
    template_name = 'login/register.html'
    success_url = reverse_lazy('base:Login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'สมัครสมาชิกสำเร็จ! กรุณารอสักครู่...')
        return super().form_valid(form)  # ใช้ super() เพื่อเรียกการทำงานปกติของ Django
    
    def form_invalid(self, form):
        messages.error(self.request, 'เกิดข้อผิดพลาดในการลงทะเบียน กรุณาตรวจสอบข้อมูลอีกครั้ง.')
        return super().form_invalid(form)

# View สำหรับการเข้าสู่ระบบ
class Userloginview(LoginView):
    template_name = 'login/login.html'
    
    def get_success_url(self):
        return reverse_lazy('base:home')

# View สำหรับแสดงรายการอุปกรณ์ในหน้า homepage
class HomepageView(ListView):
    model = Equipment
    template_name = 'homepage.html'
    context_object_name = 'equipments'
    paginate_by = 10 

# View สำหรับการรีเซ็ตรหัสผ่าน
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'login/password_reset.html'
    email_template_name = 'login/password_reset_email.html'
    subject_template_name = 'login/password_reset_subject.txt'
    success_message = 'เราได้ส่งลิงค์ในการ reset รหัสผ่านไปทางอีเมลที่คุณแจ้งแล้ว โปรดตรวจสอบที่ email ของคุณ'
    success_url = reverse_lazy('base:Login')

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

# View สำหรับแสดงรายการแจ้งเตือน
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification_list.html'
    context_object_name = 'notifications'
    
    def get_queryset(self):
        # ดึงเฉพาะการแจ้งเตือนที่ยังไม่ถูกอ่าน
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ส่งจำนวนการแจ้งเตือนที่ยังไม่ได้อ่านไปที่ template
        context['unread_count'] = Notification.objects.filter(user=self.request.user, is_read=False).count()
        return context

def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    messages.success(request, 'การแจ้งเตือนถูกทำเครื่องหมายว่าอ่านแล้ว')
    return redirect('base:notification_list')
#admin CRUD

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'user_management/user_list.html'
    context_object_name = 'users'
    
    def test_func(self):
        return self.request.user.is_superuser  

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    template_name = 'user_management/user_form.html' 
    fields = '__all__'
    success_url = reverse_lazy('base:user_list')
    
    def test_func(self):
        return self.request.user.is_superuser  

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'user_management/user_confirm_delete.html'
    success_url = reverse_lazy('base:user_list')
    
    def test_func(self):
        return self.request.user.is_superuser 

class AccountView(LoginRequiredMixin,TemplateView):
    template_name = 'dashborad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch user information
        user = self.request.user
        context['user'] = user

        # Fetch current rentals (items not yet returned)
        context['current_rentals'] = Booking.objects.filter(user=user, status='approved')

        # Fetch rental history (items returned)
        context['rental_history'] = Booking.objects.filter(user=user, status='Returned')

        return context

class BookingApprovalView(UserPassesTestMixin, ListView):
    model = Booking
    template_name = 'booking_approval_list.html'
    context_object_name = 'bookings'

    def test_func(self):
        return self.request.user.is_superuser  # ให้เฉพาะแอดมินเท่านั้นที่สามารถเข้าถึงหน้านี้ได้

    def post(self, request, *args, **kwargs):
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')  # รับ action ว่าแอดมินเลือก approved หรือ declined
        booking = get_object_or_404(Booking, id=booking_id)

        if action == 'approve':
            booking.status = 'approved'
            messages.success(request, f'Booking #{booking.id} has been approved.')
        elif action == 'decline':
            booking.status = 'declined'
            messages.warning(request, f'Booking #{booking.id} has been declined.')

        booking.save()
        return redirect('base:booking_approval')  # Redirect ไปยังหน้าการอนุมัติการจอง