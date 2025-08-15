"""
========================================================
 File: urls.py  (accounts app)
 Usage:
    Defines all URL patterns for the accounts module,
    including authentication, password reset, dashboard
    navigation, and profile management.

 Notes:
    - Uses Django's built-in auth views for password reset.
    - Each URL is given a unique name for reverse lookups.
========================================================
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ==============================
    # Authentication Routes
    # ==============================
    path('login/', views.login_view, name='login'),          # User login page
    path('logout/', views.logout_view, name='logout'),       # User logout action
    path('register/', views.register, name='register'),      # New user registration

    # ==============================
    # Password Reset (Built-in Django)
    # ==============================
    path(
        'forgot_password/',
        auth_views.PasswordResetView.as_view(
            template_name="accounts/forgot_password.html"
        ),
        name='forgot_password'
    ),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_sent.html"
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_form.html"
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name='password_reset_complete'
    ),

    # ==============================
    # User Dashboard & Profile
    # ==============================
    path('dashboard/user/', views.user_dashboard_view, name='user_dashboard'),  # Citizen dashboard home
    path('profile/', views.citizen_profile, name='citizen_profile'),            # Citizen profile view
    path('citizen/edit_profile/', views.edit_profile, name='edit_profile'),     # Edit profile form

    # ==============================
    # Complaints (to be added later)
    # ==============================
]
