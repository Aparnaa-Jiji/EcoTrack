"""
========================================================
 File: views.py  (accounts app)
 Usage:
    Handles all account-related views such as:
        - Login & Logout
        - Registration
        - Password reset (placeholder)
        - Citizen dashboard & profile management

 Notes:
    - Uses Django's built-in authentication system.
    - Role-based redirection is implemented in login_view.
    - Password reset is mostly handled via built-in Django views
      (see urls.py), except forgot_password_view is a placeholder.
========================================================
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserRegistrationForm

# ==============================
# Login View
# ==============================
def login_view(request):
    """
    Handles user login for all roles:
        - citizen
        - collector
        - admin
    Authenticates using email & password, then redirects
    to the role-appropriate dashboard.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)  # Creates user session

            # Redirect based on role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'collector':
                return redirect('collector_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'accounts/login.html')


# ==============================
# Logout View
# ==============================
def logout_view(request):
    """
    Logs out the current user and redirects to login page.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# ==============================
# Forgot Password View (Placeholder)
# ==============================
def forgot_password_view(request):
    """
    Temporary forgot-password page.
    Currently just shows a confirmation message.
    The actual password reset flow is handled by Django's
    built-in views in urls.py.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        # TODO: Implement actual password reset logic
        messages.success(request, "If this email exists, a password reset link has been sent.")
        return render(request, "accounts/forgot_password.html")
    
    return render(request, "accounts/forgot_password.html")


# ==============================
# Registration View
# ==============================
def register(request):
    """
    Registers a new user using CustomUserRegistrationForm.
    Validates input, saves the user, then redirects to login.
    """
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# ==============================
# Citizen Dashboard View
# ==============================
@login_required
def user_dashboard_view(request):
    """
    Displays the citizen's dashboard home.
    TODO:
        Replace placeholder stats with real data.
    """
    context = {
        'upcoming_pickups_count': 0,
        'total_pickups_count': 0,
        'pending_requests_count': 0,
    }
    return render(request, 'ecotracksys/user_dashboard/index.html', context)


# ==============================
# Citizen Profile View
# ==============================
@login_required
def citizen_profile(request):
    """
    Shows the logged-in user's profile details.
    """
    context = {
        'user': request.user
    }
    return render(request, 'ecotracksys/user_dashboard/my_profile.html', context)


# ==============================
# Edit Profile View
# ==============================
@login_required
def edit_profile(request):
    """
    Allows logged-in users to edit their profile.
    Supports GET (form display) and POST (save changes).
    """
    user = request.user

    if request.method == 'POST':
        user.name = request.POST.get('name', user.name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)

        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('citizen_profile')

    return render(request, 'ecotracksys/user_dashboard/edit_profile.html', {'user': user})
