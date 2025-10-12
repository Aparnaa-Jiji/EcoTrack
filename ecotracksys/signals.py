# ecotracksys/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from accounts.models import CustomUser
from .models import PickupRequest
from .models import Notification   # adjust import if your Notification model is in a different app


@receiver(post_save, sender=PickupRequest)
def notify_admins_on_pickup_request(sender, instance, created, **kwargs):
    if created:  # only when a new pickup request is created
        # get all admin users
        admins = CustomUser.objects.filter(role="admin")

        for admin in admins:
            Notification.objects.create(
                user=admin,
                title="New Pickup Request",
                message=f"Pickup requested by {instance.customer_name} on {instance.pickup_date} at {instance.pickup_time}.",
                type="info",
                status="unread",
                is_important=True,
            )

# ecotracksys/signals.py

from .models import Complaint   # adjust path if Complaint is in another app

@receiver(post_save, sender=Complaint)
def notify_admins_on_complaint(sender, instance, created, **kwargs):
    if created:
        admins = CustomUser.objects.filter(role="admin")
        for admin in admins:
            Notification.objects.create(
                user=admin,
                title="New Complaint",
                message=f"Complaint raised by {instance.user} - {instance.issue[:50]}...",
                type="warning",
                status="unread",
                is_important=True,
            )

from .models import LeaveRequest

@receiver(post_save, sender=LeaveRequest)
def notify_admins_on_leave_request(sender, instance, created, **kwargs):
    if created:
        admins = CustomUser.objects.filter(role="admin")
        for admin in admins:
            Notification.objects.create(
                user=admin,
                title="New Leave Request",
                message=f"{instance.collector} requested leave from {instance.start_date} to {instance.end_date}.",
                type="info",
                status="unread",
                is_important=False,
            )

@receiver(post_save, sender=CustomUser)
def notify_admins_on_new_user(sender, instance, created, **kwargs):
    if created and instance.role == "citizen":  # or include collector if you want
        admins = CustomUser.objects.filter(role="admin")
        for admin in admins:
            Notification.objects.create(
                user=admin,
                title="New User Registered",
                message=f"New {instance.role} registered: {instance.email}",
                type="success",
                status="unread",
                is_important=False,
            )

# notifications for collector
# ecotracksys/signals.py

from .models import PickupRequest

@receiver(post_save, sender=PickupRequest)
def notify_collector_on_assignment(sender, instance, created, **kwargs):
    # If a pickup request is assigned/updated with a collector
    if instance.collector:
        title = "Pickup Assigned" if created else "Pickup Updated"
        message = f"You have a pickup on {instance.pickup_date} at {instance.pickup_time}."

        Notification.objects.create(
            user=instance.collector,
            title=title,
            message=message,
            type="info",
            status="unread",
            is_important=True,
        )

from .models import LeaveRequest

@receiver(post_save, sender=LeaveRequest)
def notify_collector_on_leave_response(sender, instance, created, **kwargs):
    if not created:  # Only after admin updates
        status_msg = "approved ✅" if instance.status == "approved" else "rejected ❌"
        Notification.objects.create(
            user=instance.collector,
            title="Leave Request Update",
            message=f"Your leave from {instance.start_date} to {instance.end_date} was {status_msg}.",
            type="success" if instance.status == "approved" else "error",
            status="unread",
            is_important=False,
        )

def send_broadcast_to_collectors(title, message):
    collectors = CustomUser.objects.filter(role="collector")
    for collector in collectors:
        Notification.objects.create(
            user=collector,
            title=title,
            message=message,
            type="warning",
            status="unread",
        )

# citizens notification
from .models import PickupRequest, Complaint
from .models import Notification

# Citizen: Notify when they request a pickup
@receiver(post_save, sender=PickupRequest)
def notify_citizen_on_request(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            title="Pickup Request Submitted",
            message=f"Your pickup request for {instance.pickup_date} at {instance.pickup_time} has been received.",
            type="success",
            status="unread"
        )
    else:
        Notification.objects.create(
            user=instance.user,
            title="Pickup Status Updated",
            message=f"Your pickup request for {instance.pickup_date} at {instance.pickup_time} is now '{instance.status}'.",
            type="info",
            status="unread"
        )

