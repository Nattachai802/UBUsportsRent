from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    contact_number = models.CharField(max_length= 20 , blank = True)
    role = models.CharField(max_length= 50 )
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.username


class Equipment(models.Model):
    #id is primary key
    name = models.CharField(max_length = 100)
    type = models.CharField(max_length = 50)
    available_amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add= True)
    picture = models.ImageField(upload_to='equipment_pictures/', default='default.jpg')
    
    def __str__(self):
        return self.name

class Staff(models.Model):
    #id is primary key
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE ,null=True, blank=True ,related_name='staff')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Booking(models.Model):
    #id is primary key
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment , on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, 
                              choices=[
                                  ('Pending', 'Pending'), 
                                  ('Approved', 'Approved'), 
                                  ('Denied', 'Denied')
                                  ])
    approved_by = models.ForeignKey('Staff',on_delete=models.SET_NULL , null = True , blank = True)
    booking_date = models.DateTimeField()
    return_date = models.DateTimeField()

    def __str__(self):
        return f'Booking by {self.user.username} on {self.booking_date}'

class Notification(models.Model):
    #id is primary key
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username}'

class Statistics(models.Model):
    #id is primary key
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    usage_count = models.PositiveIntegerField(default=0)
    last_used = models.DateTimeField()

    def __str__(self):
        return f'Statistics for {self.equipment.name}'

class BookingHistory(models.Model):
    #id is primary key
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('approved', 'approved'), ('denied', 'denied'), ('cancelled', 'cancelled')])
    changed_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    change_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'History for Booking {self.booking.id}'

class ReturnBooking(models.Model):
    #id is primary key
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Returned', 'Returned'), ('Not Returned', 'Not Returned')])
    verified_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    return_date = models.DateTimeField()

    def __str__(self):
        return f'Return for Booking {self.booking.id}'
