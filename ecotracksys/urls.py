from django.urls import path
from . import views

app_name = 'ecotracksys'

urlpatterns = [
    # ===============================
    # PUBLIC / STATIC PAGES
    # ===============================
    # Homepage
    path('', views.home, name='index'),
    # How EcoTrack works page
    path('works/', views.works, name='works'),
    # About page
    path('about/', views.about, name='about'),
    # Contact page
    path('contact/', views.contact, name='contact'),

    # ===============================
    # CITIZEN DASHBOARD ROUTES
    # ===============================
    # Citizen dashboard home
    path('citizen/', views.citizen_dashboard, name='citizen_dashboard'),
    # Citizen - request pickup
    path('citizen/pickup-request/', views.pickup_request_view, name='citizen_pickup_request'),
    # Citizen - view pickup history
    path('citizen/history/', views.my_requests_view, name='citizen_history'),
    # Citizen - raise complaint
    path('citizen/complaints/', views.raise_complaint, name='raise_complaint'),
    # Citizen - complaint submitted successfully
    path('citizen/complaint-success/', views.complaint_success, name='complaint_success'),
    # Citizen - notifications
    path('citizen/notifications/', views.notifications_view, name='notifications_view'),
    # Citizen - update password
    path('citizen/update-password/', views.update_password, name='update_password'),
    # Citizen - profile
    path('citizen/profile/', views.citizen_profile, name='citizen_profile'),
    # Citizen - edit profile
    path('citizen/edit-profile/', views.edit_profile, name='edit_profile'),
    # Citizen - mark notification as read
    path('citizen/notifications/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    # Citizen - mark notification as unread
    path('citizen/notifications/mark-unread/', views.mark_notification_unread, name='mark_notification_unread'),
    # Citizen - delete notification
    path('citizen/notifications/delete/', views.delete_notification, name='delete_notification'),
    # Citizen - edit pickup request
    path('dashboard/citizen/edit-pickup/', views.edit_pickup_request, name='edit_pickup_request'),
    # Citizen - cancel pickup request
    path('dashboard/citizen/cancel-pickup/', views.cancel_pickup_request, name='cancel_pickup_request'),
    # Citizen - manage notifications (AJAX)
    path('citizen/notifications/<int:notif_id>/<str:action>/', views.manage_notification, name='manage_notification'),
    # Citizen - cancel pickup (duplicate path, kept intentionally)
    path('citizen/pickup-request/cancel/', views.cancel_pickup_request, name='cancel_pickup_request'),

    # ===============================
    # COLLECTOR DASHBOARD ROUTES
    # ===============================
    # Collector dashboard home
    path('collector/', views.collector_dashboard, name='collector_dashboard'),
    # Collector - assigned pickups
    path('collector/assignments/', views.collector_assignments, name='collector_assignments'),
    # Collector - pickup history
    path('collector/pickup-history/', views.collector_pickup_history, name='collector_pickup_history'),
    # Collector - performance report
    path('collector/performance/', views.collector_performance, name='collector_performance'),
    # Collector - leave request
    path('collector/leave/', views.collector_leave, name='collector_leave'),
    # Collector - notifications
    path('collector/notifications/', views.collector_notifications, name='collector_notifications'),
    # Collector - complaints assigned
    path('collector/complaints/', views.collector_complaints, name='collector_complaints'),
    # Collector - profile
    path('collector/profile/', views.collector_profile, name='collector_profile'),

    # ===============================
    # ADMIN DASHBOARD ROUTES
    # ===============================
    # Admin dashboard home
    path('admin/', views.admin_dashboard, name='admin_dashboard'),

    # --- Pickup & Zone Management ---
    path('admin/pickup-management/', views.pickup_management, name='pickup_management'),
    # --- Zone Management (extended) ---
    path("admin/zones/", views.zone_management, name="zone_management"),
    path("admin/zones/add/", views.add_zone, name="add_zone"),
    path("dashboard/admin/zones/<int:zone_id>/edit/", views.edit_zone, name="edit_zone"),
    path("dashboard/admin/zones/<int:zone_id>/delete/", views.delete_zone, name="delete_zone"),
    path("dashboard/admin/zones/<int:zone_id>/assign/", views.assign_collector, name="assign_collector"),

    # --- Leave Requests & Complaints ---
    path('admin/leave-requests/', views.leave_request_management, name='leave_request_management'),
    path('admin/complaints/', views.complaint_management, name='complaint_management'),
    path('admin/complaints/update-status/', views.update_complaint_status, name='update_complaint_status'),
    path('admin/complaints/delete/', views.delete_complaint, name='delete_complaint'),

    # --- User Management ---
    path('admin/user-management/', views.user_management, name='user_management'),
    path('admin/user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/user/edit-inline/<int:user_id>/', views.edit_user_inline, name='edit_user_inline'),

    # --- Assignments & Scheduling ---
    path("dashboard/admin/assign-collector/<int:pickup_id>/", views.assign_collector, name="assign_collector"),
    path("dashboard/admin/reschedule/<int:pickup_id>/", views.reschedule_pickup, name="reschedule_pickup"),

    # --- Collector Management ---
    path('admin/collectors/', views.collector_management, name='collector_management'),
    path('collectors/<int:pk>/edit/', views.edit_collector, name='edit_collector'),
    path('dashboard/admin/collectors/toggle-status/<int:collector_id>/', views.toggle_collector_status, name='toggle_collector_status'),
    path('admin/collector/<int:pk>/delete/', views.collector_delete, name='collector_delete'),
    # Duplicate collector routes (kept intentionally)
    path("dashboard/admin/collectors/", views.collector_management, name="collector_management"),
    path("dashboard/admin/collectors/edit/<int:pk>/", views.edit_collector, name="edit_collector"),

    # --- Analytics, Profile & Settings ---
    path('admin/analytics/', views.analytics, name='analytics'),
    path('admin/profile/', views.admin_profile, name='admin_profile'),

    # --- Pickup Management (duplicate path kept) ---
    path('dashboard/admin/pickup-management/', views.pickup_management, name='pickup_management'),
    # --- Update Pickup Status ---
    path('dashboard/admin/update-status/<int:pickup_id>/', views.update_status, name='update_status'),
    # --- Pickup details (JSON) ---
    path('dashboard/admin/pickup/<int:pk>/details/', views.pickup_details_json, name="pickup_details"),

    
]
