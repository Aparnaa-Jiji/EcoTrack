# miniproject/ecotrack/ecotracksys/models.py

from django.db import models
from django.conf import settings
from django.utils.timezone import now

# =========================
# PickupRequest Model
# =========================
from django.db import models
from django.conf import settings

class PickupRequest(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_IN_PROGRESS = 'In Progress'
    STATUS_COMPLETED = 'Completed'
    STATUS_CANCELLED = 'Cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    WASTE_TYPES = [
        ('organic', 'Biodegradable / Organic Waste'),
        ('recyclable', 'Recyclable Waste'),
        ('nonrecyclable', 'Non-Recyclable / Residual Waste'),
        ('ewaste', 'E-Waste'),
        ('hazardous', 'Hazardous Waste'),
        ('construction', 'Construction & Demolition Waste'),
    ]

    WASTE_COST = {
        'organic': 20,
        'recyclable': 15,
        'nonrecyclable': 25,
        'ewaste': 30,
        'hazardous': 50,
        'construction': 40,
    }

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    pickup_time_slot = models.CharField(max_length=20, blank=True)
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    special_instructions = models.TextField(blank=True, default='')
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=[('Pending','Pending'),('In-Progress','In Progress'),('Completed','Completed'),('Cancelled','Cancelled')], default='Pending')
    price = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pickup_requests'
    )
    collector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': 'collector'},
        related_name='assigned_requests'
    )

    def save(self, *args, **kwargs):
        # Auto-calculate price based on waste type
        self.price = self.WASTE_COST.get(self.waste_type, 0) * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.pickup_date} {self.pickup_time} ({self.status})"


# =========================
# Complaint Model
# =========================
class Complaint(models.Model):
    """
    Stores complaints submitted by users regarding pickup or service issues.
    """

    COMPLAINT_TYPE_CHOICES = [
        ('pickup_delay', 'Pickup Delay'),
        ('misbehavior', 'Misbehavior'),
        ('incomplete_pickup', 'Incomplete Pickup'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPE_CHOICES)
    related_pickup = models.ForeignKey(
        PickupRequest,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='complaints'
    )
    description = models.TextField()
    photo = models.ImageField(upload_to='complaint_photos/', blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    date_submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_submitted']

    def __str__(self):
        return f"{self.subject} by {self.user.email}"


# =========================
# Notification Model
# =========================
class Notification(models.Model):
    """
    Stores notifications for users.
    """

    STATUS_CHOICES = [('unread', 'Unread'), ('read', 'Read')]
    TYPE_CHOICES = [('info', 'Info'), ('success', 'Success'), ('warning', 'Warning'), ('error', 'Error')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification({self.title}) for {self.user.email}"


# =========================
# LeaveRequest Model
# =========================
class LeaveRequest(models.Model):
    """
    Stores leave requests submitted by waste collectors.
    """

    LEAVE_TYPES = [('Sick', 'Sick Leave'), ('Casual', 'Casual Leave'), ('Annual', 'Annual Leave'), ('Other', 'Other')]
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]

    collector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'collector'},
        related_name='leave_requests'
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.collector.email} - {self.leave_type} ({self.status})"


# =========================
# Collector Model (Optional)
# =========================
class Collector(models.Model):
    """
    Stores collector profiles independent of main user accounts (optional).
    """

    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive')]

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    zone = models.CharField(max_length=120)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.zone})"


# =========================
# Zone Model
# =========================
class Zone(models.Model):
    name = models.CharField(max_length=100)
    ward = models.CharField(max_length=50, default='default_ward')
    collector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'collector'},
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='zones_assigned'  # avoids clash with CustomUser.zone
    )

    # Coordinates to define zone boundaries
    lat_min = models.FloatField(default=0.0)
    lat_max = models.FloatField(default=0.0)
    lng_min = models.FloatField(default=0.0)
    lng_max = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} - Ward {self.ward}"
