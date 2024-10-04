from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
app_name = 'Chat'

urlpatterns = [
    path('rooms/', views.chat_rooms, name='chat_rooms'),
    path('rooms/create/', views.create_room, name='create_room'),
    path('rooms/<str:room_name>/', views.chat_room, name='chat_room'),
]