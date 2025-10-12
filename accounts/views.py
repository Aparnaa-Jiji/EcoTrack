# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserRegistrationForm
from .models import CustomUser
from django.http import HttpResponseForbidden
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required



# =========================
# User Registration (Citizen Only)
# =========================
def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Let form assign all fields including name
            user = form.save(commit=False)
            user.role = 'citizen'  # enforce citizen role
            user.save()  # now all fields, including name, are saved
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

# =========================
# User Login
# =========================

def login_view(request):
    """
    Handles login and redirects user based on their role.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('ecotracksys:admin_dashboard')
            elif user.role == 'collector':
                return redirect('ecotracksys:collector_assignments')
            else:
                return redirect('ecotracksys:citizen_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')


# =========================
# User Logout
# =========================
def logout_view(request):
    request.session.flush()  # Clear session data
    logout(request)
    return redirect('login')


# =========================
# Dashboards
# =========================
@login_required
def user_dashboard_view(request):
    """Citizen dashboard"""
    return render(request, 'ecotracksys/user_dashboard/index.html')


@login_required
def collector_dashboard_view(request):
    if request.user.role != 'collector':
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'ecotracksys/collector_dashboard/collector_dashboard.html')

@login_required
def admin_dashboard_view(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'ecotracksys/admin_dashboard/index.html')


# =========================
# Profile Views (Citizen)
# =========================




