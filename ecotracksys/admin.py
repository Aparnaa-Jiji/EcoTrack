# ecotracksys/admin.py
from time import timezone
from django.contrib import admin
from .models import PickupRequest, Complaint, Notification, LeaveRequest, Collector

# -------------------------
# PickupRequest Admin
# -------------------------
@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'pickup_date', 'pickup_time', 'waste_type', 'status', 'collector')
    list_filter = ('status', 'waste_type', 'pickup_date')
    search_fields = ('customer_name', 'email', 'phone', 'address')
    ordering = ('-pickup_date',)

# -------------------------
# Complaint Admin
# -------------------------
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'complaint_type', 'status', 'date_submitted')
    list_filter = ('complaint_type', 'status', 'date_submitted')
    search_fields = ('subject', 'description', 'user__email')
    ordering = ('-date_submitted',)

# -------------------------
# Notification Admin
# -------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'status', 'is_important', 'created_at')
    list_filter = ('type', 'status', 'is_important', 'created_at')
    search_fields = ('title', 'message', 'user__email')
    ordering = ('-created_at',)

# -------------------------
# LeaveRequest Admin
# -------------------------

# ecotracksys/admin.py
from django.contrib import admin
from .models import LeaveRequest
from django.utils import timezone

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('collector', 'leave_type', 'start_date', 'end_date', 'status', 'applied_at')
    list_filter = ('status', 'leave_type', 'applied_at')
    search_fields = ('collector__email', 'collector__first_name', 'collector__last_name')
    readonly_fields = ('applied_at', 'reviewed_at')
    actions = ['mark_approved', 'mark_rejected']

    def mark_approved(self, request, queryset):
        queryset.update(status='Approved', reviewed_at=timezone.now())
    mark_approved.short_description = "Mark selected as approved"

    def mark_rejected(self, request, queryset):
        queryset.update(status='Rejected', reviewed_at=timezone.now())
    mark_rejected.short_description = "Mark selected as rejected"
    
# -------------------------
# Collector Admin
# -------------------------
@admin.register(Collector)
class CollectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'zone', 'status', 'created_at')
    list_filter = ('status', 'zone')
    search_fields = ('name', 'phone', 'zone')
    ordering = ('name',)
