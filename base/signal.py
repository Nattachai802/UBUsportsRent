from .models import CustomUser ,Staff , Notification , Booking
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_staff_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Staff.objects.create(user=instance)

        
@receiver(post_save, sender=CustomUser)
def save_staff_for_superuser(sender, instance, **kwargs):
    if instance.is_superuser:
        if not hasattr(instance, 'staff'):  # ตรวจสอบว่า CustomUser มี Staff หรือไม่
            Staff.objects.create(user=instance)  # สร้าง Staff ถ้ายังไม่มี
        instance.staff.save()  # บันทึกข้อมูล staff

@receiver(post_save, sender=Booking)
def create_booking_notification(sender, instance, created, **kwargs):
    if created:
        message = f'Your booking for {instance.equipment.name} has been confirmed.'
        Notification.objects.create(user=instance.user, message=message)

def create_return_notification(sender, instance, **kwargs):
    if instance.return_date:  # Assuming you have a 'returned' field in the Booking model
        message = f'You have successfully returned {instance.equipment.name}.'
        Notification.objects.create(user=instance.user, message=message)


@receiver(post_save, sender=Booking)
def notify_admins_about_booking(sender, instance, created, **kwargs):
    if created:
        admin_users = CustomUser.objects.filter(is_superuser=True)
        for admin in admin_users:
            message = f'A new booking for {instance.equipment.name} has been made by {instance.user.username}.'
            Notification.objects.create(user=admin, message=message)