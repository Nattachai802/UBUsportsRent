from django.urls import path , include
from base.views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
app_name = 'base'

urlpatterns = [
    path('account/', AccountView.as_view(), name='account_dashboard'),
    path('booking-approval/', BookingApprovalView.as_view(), name='booking_approval'),
    
    path('', HomepageView.as_view() , name='home' ),
    path('signup/', UserRegisterview.as_view(), name='Register'),
    path('login/', Userloginview.as_view() , name='Login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('base:Login')), name='logout'),
    
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='login/password_reset_confirm.html',
                                                     success_url=reverse_lazy('base:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
        template_name='login/password_reset_complete.html'),
         name='password_reset_complete'),
    
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:notification_id>/read/', mark_as_read, name='mark_as_read'),
    
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    
    path('api/bookings/', booking_events, name='booking_events'),

]
