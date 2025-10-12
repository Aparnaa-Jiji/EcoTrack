from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'ecotracksys'

urlpatterns = [
    # ===============================
    # PUBLIC / STATIC PAGES
    # ===============================
    path('', views.home, name='index'),                         # Homepage
    path('works/', views.works, name='works'),                  # How EcoTrack works
    path('about/', views.about, name='about'),                  # About page
    path('contact/', views.contact, name='contact'),            # Contact page

    # ===============================
    # CITIZEN DASHBOARD ROUTES
    # ===============================
    path('citizen/', views.citizen_dashboard, name='citizen_dashboard'),                  # Dashboard home
    path('citizen/pickup-request/', views.pickup_request_view, name='citizen_pickup_request'),  # Request pickup
    path('citizen/history/', views.my_requests_view, name='citizen_history'),            # View pickup history
    path('citizen/complaints/', views.raise_complaint, name='raise_complaint'),          # Raise complaint
    path('citizen/complaint-success/', views.complaint_success, name='complaint_success'), # Complaint success
    path('citizen/notifications/', views.notifications_view, name='notifications_view'), # View notifications
    path('citizen/update-password/', views.update_password, name='update_password'),    # Update password
    path('citizen/profile/', views.citizen_profile, name='citizen_profile'),            # View profile
    path('citizen/edit-profile/', views.edit_profile, name='edit_profile'),             # Edit profile

    # Citizen notification management
    path('citizen/notifications/delete/', views.delete_notification, name='delete_notification'),   # Delete notification
    path('citizen/notifications/<int:notif_id>/<str:action>/', views.manage_notification, name='manage_notification'), # AJAX: mark read/unread
    path('citizen/pickup-request/cancel/', views.cancel_pickup_request, name='cancel_pickup_request'), # Cancel pickup (intentional duplicate)

    # Citizen pickup editing
    path('dashboard/citizen/edit-pickup/', views.edit_pickup_request, name='edit_pickup_request'),
    path('dashboard/citizen/cancel-pickup/', views.cancel_pickup_request, name='cancel_pickup_request'),

    # ===============================
    # COLLECTOR DASHBOARD ROUTES
    # ===============================
    path('collector/', views.collector_dashboard, name='collector_dashboard'),  # Dashboard home

    # Collector assignments
    path('collector/assignments/', views.collector_assignments, name='collector_assignments'),
    path('collector/assignment/<int:assignment_id>/update/', views.update_assignment_status, name='update_assignment_status'),
    path('collector/pickup-history/', views.collector_pickup_history, name='collector_pickup_history'),
    path('collector/performance/', views.collector_performance, name='collector_performance'),

    # Collector profile & settings
    path('collector/profile/', views.collector_profile, name='collector_profile'),
    path('collector/change-password/', views.collector_change_password, name='collector_change_password'),
    path('collector/leave/', views.collector_leave, name='collector_leave'),
    path('collector/leave/<int:leave_id>/cancel/', views.cancel_leave, name='collector_cancel_leave'),
    path('collector/complaints/', views.collector_complaints, name='collector_complaints'),

    # Collector shift management (API)
    path('api/collector/shift/start/', views.start_shift, name='collector_shift_start'),
    path('api/collector/shift/end/', views.end_shift, name='collector_shift_end'),

    # Collector assignment actions (API)
    path('dashboard/collector/assignment/<int:pk>/start/', views.collector_start_assignment, name='collector_start_assignment'),
    path('dashboard/collector/assignment/<int:pk>/enroute/', views.collector_enroute_assignment, name='collector_enroute_assignment'),
    path('dashboard/collector/assignment/<int:pk>/complete/', views.collector_complete_assignment, name='collector_complete_assignment'),
    path('api/collector/assignment/<int:job_id>/issue/', views.raise_issue, name='raise_issue'),

    # Collector notifications
    path('dashboard/collector/notifications/', views.collector_notifications, name='collector_notifications'),

    # Collector pickup status update
    path('collector/update-status/<int:pickup_id>/<str:new_status>/', views.update_pickup_status, name='update_pickup_status'),
    path('collector/complete_pickup/', views.complete_pickup, name='complete_pickup'),

    # ===============================
    # ADMIN DASHBOARD ROUTES
    # ===============================
    path('admin/', views.admin_dashboard, name='admin_dashboard'),  # Dashboard home

    # --- Pickup & Zone Management ---
    path('admin/pickup-management/', views.pickup_management, name='pickup_management'),
    path('dashboard/admin/pickup-management/', views.pickup_management, name='pickup_management'),  # duplicate
    path('dashboard/admin/update-status/<int:pickup_id>/', views.update_status, name='update_status'),
    path('dashboard/admin/pickup/<int:pk>/details/', views.pickup_details_json, name="pickup_details"),

    # --- Leave Requests ---
    path('admin/leave-requests/', views.leave_request_management, name='leave_request_management'),
    path('admin/leave-requests/<int:leave_id>/<str:action>/', views.update_leave_status, name='update_leave_status'),
    path('admin/leave-requests/action/', views.leave_request_action, name='leave_request_action'),
    path('admin/leave-requests/ajax-action/', views.leave_request_action_ajax, name='leave_request_action_ajax'),

    # --- Complaints ---
    path('admin/complaints/', views.complaint_management, name='complaint_management'),
    path('admin/complaints/update-status/', views.update_complaint_status, name='update_complaint_status'),
    path('admin/complaints/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),

    # --- User Management ---
    path('admin/user-management/', views.user_management, name='user_management'),
    path('admin/user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/user/edit-inline/<int:user_id>/', views.edit_user_inline, name='edit_user_inline'),

    # --- Collector Management ---
    path('admin/collectors/', views.collector_management, name='collector_management'),
    path('dashboard/admin/collectors/', views.collector_management, name='collector_management'),  # duplicate
    path('collectors/<int:pk>/edit/', views.edit_collector, name='edit_collector'),
    path('dashboard/admin/collectors/edit/<int:pk>/', views.edit_collector, name='edit_collector'),  # duplicate
    path('dashboard/admin/collectors/toggle-status/<int:collector_id>/', views.toggle_collector_status, name='toggle_collector_status'),
    path('admin/collector/<int:pk>/delete/', views.collector_delete, name='collector_delete'),
    path('collector/delete/<int:collector_id>/', views.delete_collector, name='delete_collector'),

    # --- Assignments & Scheduling ---
    path('admin/assign-collector/<int:pickup_id>/', views.assign_collector, name='assign_collector'),
    path('reschedule_pickup/<int:pickup_id>/', views.reschedule_pickup, name='reschedule_pickup'),

    # --- Analytics ---
    path('analytics/', views.analytics_view, name='analytics'),
    path('admin/analytics/', views.admin_analytics, name='admin_analytics'),

    # --- Admin profile ---
    path('admin/profile/', views.admin_profile, name='admin_profile'),

    # ===============================
    # NOTIFICATIONS ROUTES (ALL USERS)
    # ===============================
    # Bulk delete notifications
    path('notifications/delete-selected/', views.delete_selected_notifications, name='delete_selected_notifications'),
    # Single delete
    path('api/admin/notifications/<int:pk>/delete/', views.delete_notification, name='delete_notification'),
    path('api/notifications/<int:notif_id>/toggle_read/', views.toggle_read_notification, name='toggle_read_notification'),
    path('api/notifications/<int:notif_id>/delete/', views.delete_notification, name='delete_notification'),
    # Admin notification management
    path('dashboard/admin/notifications/', views.admin_notifications, name='admin_notifications'),
    path('notifications/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-unread/', views.mark_notification_unread, name='mark_notification_unread'),
    path('notifications/delete/', views.delete_notification, name='delete_notification'),

    # Citizen notifications (duplicate route)
    path('citizen/notifications/', views.citizen_notifications, name='citizen_notifications'),
]
