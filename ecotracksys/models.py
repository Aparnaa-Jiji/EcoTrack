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
    STATUS_IN_PROGRESS = 'In-Progress'
    STATUS_COMPLETED = 'Completed'
    STATUS_CANCELLED = 'Cancelled'
    STATUS_MISSED = 'Missed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_MISSED, 'Missed'),]

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
    status = models.CharField(max_length=20, choices=[('Pending','Pending'),('In-Progress','In Progress'),('Completed','Completed'),('Cancelled','Cancelled'),('Missed','Missed')], default='Pending')
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
    # New fields
    assigned_collector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'collector'},
        related_name='assigned_pickups'
    )
    otp = models.CharField(max_length=6, blank=True, null=True)

    def assign_collector(self, collector):
        """Assign a collector and generate a 6-digit OTP."""
        self.assigned_collector = collector
        self.otp = f"{random.randint(100000, 999999)}"
        self.save()

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
# ecotracksys/models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Sick', 'Sick'),
        ('Casual', 'Casual'),
        ('Annual', 'Annual'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    collector = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='leaves',
        limit_choices_to={'role': 'collector'},
        help_text="Collector who applied for leave"
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.collector.email} — {self.leave_type} ({self.start_date} to {self.end_date})"

    def clean(self):
        # Basic validation so start_date <= end_date
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({'end_date': "The 'end' date must be the same as or after the 'start' date."})

    @property
    def days(self):
        """Return number of days (inclusive)."""
        return (self.end_date - self.start_date).days + 1

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

from django.db import models
from django.conf import settings

class Issue(models.Model):
    pickup_request = models.ForeignKey(
        "PickupRequest", on_delete=models.CASCADE, related_name="issues"
    )
    collector = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="collector_issues"
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("open", "Open"), ("resolved", "Resolved")],
        default="open"
    )

    def __str__(self):
        return f"Issue #{self.id} for Pickup {self.pickup_request_id}"

from django.conf import settings
from django.db import models
from django.utils import timezone

class CollectorShift(models.Model):
    collector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def end_shift(self):
        self.end_time = timezone.now()
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.collector.email} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    