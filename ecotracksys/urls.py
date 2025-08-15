from django.urls import path
from . import views  # Import views from ecotracksys app

from django.urls import path
from . import views

urlpatterns = [
    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/pickup-management/', views.pickup_management, name='pickup_management'),
    path('admin/zone-management/', views.zone_management, name='zone_management'),
    path('admin/leave-requests/', views.leave_request_management, name='leave_req_management'),
    path('admin/complaints/', views.complaint_management, name='complaint_management'),
    path('admin/user_management/', views.user_management, name='user_management'),
    path('admin/collectors/', views.collector_management, name='collector_management'),
    path('admin/analytics/', views.analytics, name='analytics'),
    path('admin/profile/', views.admin_profile, name='admin_profile'),
    path('admin/settings/', views.system_setting, name='system_setting'),

    # Collector Dashboard
    path('collector/', views.collector_dashboard, name='collector_dashboard'),
    path('collector/today-tasks/', views.today_tasks, name='today_tasks'),
    path('collector/history/', views.pickup_history, name='pickup_history'),
    path('collector/leave/', views.collector_leave_request, name='collector_leave'),

    # Citizen Dashboard
    path('citizen/', views.citizen_dashboard, name='citizen_dashboard'),
    path('citizen/pickup-request/', views.citizen_pickup_request, name='citizen_pickup_request'),
    path('citizen/history/', views.citizen_history, name='citizen_history'),
]
