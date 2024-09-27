from .models import CustomUser ,Staff , Notification , Booking
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


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
        send_mail(
            'Booking Confirmation - UBU Sports Rent',
            message,  # The message to send
            settings.DEFAULT_FROM_EMAIL,  # From email
            [instance.user.email],  # To email (user's email)
            fail_silently=False,)

def create_return_notification(sender, instance, **kwargs):
    if instance.return_date and instance.status == 'Returned':  # Assuming you have a 'returned' field in the Booking model
        message = f'You have successfully returned {instance.equipment.name}.'
        Notification.objects.create(user=instance.user, message=message)
        send_mail(
            'Return Confirmation - UBU Sports Rent',
            message,  # The message to send
            settings.DEFAULT_FROM_EMAIL,  # From email
            [instance.user.email],  # To email (user's email)
            fail_silently=False,
        )


@receiver(post_save, sender=Booking)
def notify_admins_about_booking(sender, instance, created, **kwargs):
    if created:
        admin_users = CustomUser.objects.filter(is_superuser=True)
        for admin in admin_users:
            message = f'A new booking for {instance.equipment.name} has been made by {instance.user.username}.'
            Notification.objects.create(user=admin, message=message)

@receiver(post_save, sender=Booking)
def notify_booking_status_change(sender, instance, **kwargs):
    # Check for different statuses
    if instance.status == 'approved':
        message = f'Your booking for {instance.equipment.name} has been approved!'
    elif instance.status == 'declined':
        message = f'Your booking for {instance.equipment.name} has been declined.'
    else:
        message = f'Your booking for {instance.equipment.name} is in pending status.'
    
    # Create the notification
    Notification.objects.create(user=instance.user, message=message)