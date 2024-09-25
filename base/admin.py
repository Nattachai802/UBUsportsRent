
from django.contrib import admin
from .models import CustomUser 

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_staff')  # กำหนดฟิลด์ที่จะแสดง
