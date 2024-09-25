from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.contrib.auth.views import LoginView, LogoutView , PasswordResetView
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from base.models import *
from base.form import UserRegisterForms
# Create your views here.

class UserRegisterview(CreateView):
    form_class = UserRegisterForms
    template_name = r'login/register.html'
    success_url = reverse_lazy('base:login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'สมัครสมาชิกสำเร็จ! กรุณารอสักครู่...')
        return self.render_to_response(self.get_context_data(form=form))
    
    def form_invalid(self , form):
        messages.error(self.request, 'เกิดข้อผิดพลาดในการลงทะเบียน กรุณาตรวจสอบข้อมูลอีกครั้ง.')
        return self.render_to_response(self.get_context_data(form=form))

class Userloginview(LoginView):
    template_name = 'login/login.html'
    
    def get_success_url(self):
        return reverse_lazy('base:home')

class HomepageView(ListView):
    model = Equipment
    template_name = 'homepage.html'
    context_object_name = 'equipments'
    paginate_by = 10 

class ResetPasswordView(SuccessMessageMixin,PasswordResetView):
    template_name = 'login/password_reset.html'
    email_template_name = 'login/password_reset_email.html'
    subject_template_name = 'login/password_reset_subject.txt'
    success_message = 'เราได้ส่งลิงค์ในการ reset รหัสผ่านไปทางอีเมลที่คุณแจ้งแล้ว โปรดตรวจสอบที่emailของคุณ'
    success_url = reverse_lazy('base:Login')
    def form_valid(self, form):
        messages.success(self.request , self.success_message)
        return super().form_valid(form)

def notification_list_view(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notification_list.html', {'notifications': notifications})


    

