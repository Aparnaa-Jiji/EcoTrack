#ecotracksys/models.py
from django.db import models
from accounts.models import CustomUser
from django.conf import settings


class PickupRequest(models.Model):
    WASTE_TYPES = [
        ('organic', 'Organic'),
        ('recyclable', 'Recyclable'),
        ('hazardous', 'Hazardous'),
        ('mixed', 'Mixed'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In-Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    special_instructions = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    pickup_time_slot = models.CharField(max_length=20, blank=True)  # or maybe a choice field
    quantity = models.PositiveIntegerField(default=1)
    collector = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_requests')
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pickup_requests')
    special_instructions = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.customer_name} - {self.pickup_date} {self.pickup_time}"

from django.db import models
from django.conf import settings

class Complaint(models.Model):
    COMPLAINT_TYPE_CHOICES = [
        ('pickup_delay', 'Pickup Delay'),
        ('misbehavior', 'Misbehavior'),
        ('incomplete_pickup', 'Incomplete Pickup'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPE_CHOICES)
    related_pickup = models.CharField(max_length=50, blank=True, null=True)  # or ForeignKey to PickupRequest if exists
    description = models.TextField()
    photo = models.ImageField(upload_to='complaint_photos/', blank=True, null=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.subject} by {self.user.email}"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
    ]

    TYPE_CHOICES = [
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification({self.title}) for {self.user.email}"
