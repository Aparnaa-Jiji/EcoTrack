# ============================================================
# ecotracksys/views.py
# Fully reordered and commented (all original functions preserved — duplicates kept).
# ============================================================

from datetime import timedelta
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from .models import PickupRequest
import json
from .models import PickupRequest, Notification, LeaveRequest, Complaint, Zone
from .forms import ComplaintForm
from django.contrib.auth.hashers import make_password

# ============================================================
# 1. PUBLIC / STATIC PAGES
# ============================================================

# Landing page — public
def home(request):
    return render(request, 'ecotracksys/landing_page/index.html')

# Works / How it works page — public
def works(request):
    return render(request, 'ecotracksys/landing_page/works.html')

# About page — public
def about(request):
    return render(request, 'ecotracksys/landing_page/about.html')

# Contact page — public
def contact(request):
    return render(request, 'ecotracksys/landing_page/contact.html')


# ============================================================
# 2. CITIZEN VIEWS
# ============================================================

# Citizen dashboard — requires login
@login_required
def citizen_dashboard(request):
    return render(request, 'ecotracksys/user_dashboard/index.html')

# Citizen profile view — requires login
@login_required
def citizen_profile(request):
    return render(request, 'ecotracksys/user_dashboard/my_profile.html')

# --------------------
# Pickup request (citizen)
# --------------------
# NOTE: Several imports above are duplicated; kept as in original to avoid changing code.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PickupRequest, Zone

from datetime import datetime


from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PickupRequest

# Create a new pickup request — handles POST form submission and validation
@login_required
def pickup_request_view(request):
    if request.method == "POST":
        user = request.user

        # Extract form data
        customer_name = request.POST.get("customer_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        waste_type = request.POST.get("waste_type")
        pickup_date = request.POST.get("pickup_date")
        pickup_time_from_str = request.POST.get("pickup_time_from")
        pickup_time_to_str = request.POST.get("pickup_time_to")
        quantity = request.POST.get("quantity") or 1
        special_instructions = request.POST.get("special_instructions", "")

        # Validate pickup times
        if not pickup_time_from_str or not pickup_time_to_str:
            messages.error(request, "❌ Please select both pickup times.")
            return redirect('ecotracksys:citizen_pickup_request')

        try:
            pickup_time_from = datetime.strptime(pickup_time_from_str, "%H:%M").time()
            pickup_time_to = datetime.strptime(pickup_time_to_str, "%H:%M").time()
        except ValueError:
            messages.error(request, "❌ Invalid time format.")
            return redirect('ecotracksys:citizen_pickup_request')

        if pickup_time_from >= pickup_time_to:
            messages.error(request, '❌ "From" time must be earlier than "To" time.')
            return redirect('ecotracksys:citizen_pickup_request')

        # Validate location
        if not lat or not lng:
            messages.error(request, '❌ Please select a location on the map.')
            return redirect('ecotracksys:citizen_pickup_request')

        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            messages.error(request, '❌ Invalid latitude or longitude.')
            return redirect('ecotracksys:citizen_pickup_request')

        # Create PickupRequest without zone check
        PickupRequest.objects.create(
            user=user,
            customer_name=customer_name,
            phone=phone,
            email=email,
            address=address,
            lat=lat,
            lng=lng,
            waste_type=waste_type,
            pickup_date=pickup_date,
            pickup_time=pickup_time_from,
            pickup_time_slot=f"{pickup_time_from_str} - {pickup_time_to_str}",
            quantity=int(quantity),
            special_instructions=special_instructions
        )

        messages.success(request, "✅ Pickup request created successfully!")
        return redirect('ecotracksys:citizen_pickup_request')

    # GET request
    return render(request, 'ecotracksys/user_dashboard/pickup_request.html')

# Citizen — view list of their requests
@login_required
@login_required
def my_requests_view(request):
    user = request.user
    requests = PickupRequest.objects.filter(user=user).order_by('-pickup_date', '-created_at')
    return render(request, 'ecotracksys/user_dashboard/my_requests.html', {'requests': requests})

# --------------------
# Edit pickup request (AJAX / JSON endpoint)
# --------------------
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PickupRequest
import json

# Edit pickup request — expects JSON body with updates
@login_required
@csrf_exempt
def edit_pickup_request(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        pickup_request = PickupRequest.objects.get(id=request_id, user=request.user)

        if pickup_request.status in ['Cancelled', 'Completed']:
            return JsonResponse({'error': f'Request is already {pickup_request.status.lower()}.'}, status=400)

        # Convert date string to date object
        pickup_date_str = data.get('pickup_date')
        if pickup_date_str:
            pickup_request.pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date()

        # Convert time strings to time objects if needed
        time_from_str = data.get('pickup_time_from')
        time_to_str = data.get('pickup_time_to')
        if time_from_str and time_to_str:
            pickup_request.pickup_time_slot = f"{time_from_str} - {time_to_str}"

        # Update other fields
        pickup_request.waste_type = data.get('waste_type', pickup_request.waste_type)
        pickup_request.quantity = int(data.get('quantity', pickup_request.quantity))
        pickup_request.special_instructions = data.get('special_instructions', pickup_request.special_instructions)

        pickup_request.save()

        return JsonResponse({'success': True, 'message': 'Pickup request updated successfully.'})

    except PickupRequest.DoesNotExist:
        return JsonResponse({'error': 'Pickup request not found.'}, status=404)
    except ValueError as ve:
        return JsonResponse({'error': f'Invalid data format: {ve}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# --------------------
# Cancel pickup request (AJAX)
# --------------------
@login_required
@require_POST

def cancel_pickup_request(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not request_id:
        return JsonResponse({'error': 'Request ID missing'}, status=400)

    pickup_request = get_object_or_404(PickupRequest, id=request_id, user=request.user)
    if pickup_request.status in ['Cancelled', 'Completed']:
        return JsonResponse({'error': f'Request is already {pickup_request.status.lower()}.'}, status=400)

    pickup_request.status = 'Cancelled'
    pickup_request.save()
    return JsonResponse({'success': True, 'message': 'Pickup request cancelled.'})

# --------------------
# Edit profile (citizen)
# --------------------
@login_required
def edit_profile(request):
    if request.method == "POST":
        request.user.name = request.POST.get("name")
        request.user.email = request.POST.get("email")
        request.user.phone = request.POST.get("phone")
        request.user.zone = request.POST.get("zone")
        request.user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('ecotracksys:citizen_profile')

    return render(request, 'ecotracksys/user_dashboard/edit_profile.html')

# --------------------
# Citizen — raise complaint (form)
# --------------------
@login_required
@login_required
def raise_complaint(request):
    # Handle form submission
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, "Your complaint has been submitted successfully.")
            return redirect('ecotracksys:raise_complaint')
    else:
        form = ComplaintForm()
    
    # Filter related_pickup to user's pickups
    form.fields['related_pickup'].queryset = PickupRequest.objects.filter(user=request.user)
    
    # Get past complaints of the logged-in user
    past_complaints = Complaint.objects.filter(user=request.user)

    return render(request, 'ecotracksys/user_dashboard/raise_complaint.html', {
        'form': form,
        'past_complaints': past_complaints
    })

# Complaint submission success page
@login_required
def complaint_success(request):
    return render(request, 'ecotracksys/user_dashboard/complaint_success.html')

# Citizen complaint history
@login_required
def complaint_history(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-date_submitted')
    return render(request, 'ecotracksys/user_dashboard/complaint_history.html', {'complaints': complaints})


# ============================================================
# 3. NOTIFICATIONS
# ============================================================

# Notifications list — user-specific
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'notifications': notifications,
        'total_count': notifications.count(),
        'unread_count': notifications.filter(status='unread').count(),
        'today_count': notifications.filter(created_at__date=now().date()).count(),
        'important_count': notifications.filter(is_important=True).count(),
    }
    return render(request, 'ecotracksys/user_dashboard/notifications.html', context)

# Manage a single notification (mark read/unread/delete)
@login_required
@require_POST
def manage_notification(request, notif_id, action):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    if action == "read":
        notif.status = "read"
        notif.save()
    elif action == "unread":
        notif.status = "unread"
        notif.save()
    elif action == "delete":
        notif.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": True})


# ============================================================
# 4. PASSWORD MANAGEMENT
# ============================================================

# Update password for logged-in users
@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'ecotracksys/user_dashboard/update_password.html', {'form': form})


# ============================================================
# 5. ADMIN DASHBOARD & MANAGEMENT
# ============================================================

# Admin dashboard overview — staff-only
@staff_member_required
def admin_dashboard(request):
    total_pickup_requests = PickupRequest.objects.count()
    completed_pickups = PickupRequest.objects.filter(status="Completed").count()
    active_pickups = PickupRequest.objects.filter(status="In-Progress").count()
    new_pickup_requests = PickupRequest.objects.filter(status="Pending").count()
    missed_pickups = PickupRequest.objects.filter(status="Cancelled").count()
    new_complaints = Complaint.objects.filter(status="Pending").count()
    new_leave_requests = LeaveRequest.objects.filter(status="Pending").count()
    last_week = now() - timedelta(days=7)
    new_collectors = CustomUser.objects.filter(role="collector", date_joined__gte=last_week).count()
    system_alerts = Notification.objects.filter(is_important=True, status="unread").count()
    active_collectors = CustomUser.objects.filter(role="collector", is_active=True).count()
    collectors_on_leave_today = LeaveRequest.objects.filter(
        start_date__lte=now().date(), end_date__gte=now().date(), collector__role='collector', status='Approved'
    ).count()

    context = {
        "total_pickup_requests": total_pickup_requests,
        "completed_pickups": completed_pickups,
        "active_pickups": active_pickups,
        "new_pickup_requests": new_pickup_requests,
        "missed_pickups": missed_pickups,
        "new_complaints": new_complaints,
        "new_leave_requests": new_leave_requests,
        "new_collectors": new_collectors,
        "system_alerts": system_alerts,
        "active_collectors": active_collectors,
        "collectors_on_leave_today": collectors_on_leave_today,
    }
    return render(request, "ecotracksys/admin_dashboard/admin_dashboard.html", context)


# Admin-only check helper (used by decorators)
def admin_required(user):
    return user.is_authenticated and user.role == 'admin'

# Pickup management — admin view
@login_required
@user_passes_test(admin_required)
def pickup_management(request):
    pickups = PickupRequest.objects.all().order_by('-pickup_date', '-pickup_time')
    collectors = CustomUser.objects.filter(role='collector')
    context = {
        'pickups': pickups,
        'collectors': collectors
    }
    return render(request, 'ecotracksys/admin_dashboard/pickup_management.html', context)

# Assign collector to pickup — admin
@login_required
@user_passes_test(admin_required)
def assign_collector(request, pickup_id):
    pickup = get_object_or_404(PickupRequest, id=pickup_id)

    if request.method == 'POST':
        collector_id = request.POST.get('collector_id')
        collector = get_object_or_404(CustomUser, id=collector_id, role='collector')
        pickup.assigned_collector = collector
        pickup.save()
        messages.success(request, f"Collector {collector.get_full_name()} assigned successfully!")
        return redirect('pickup_management')  # or wherever the admin comes from

    collectors = CustomUser.objects.filter(role='collector')
    return render(request, 'admin_dashboard/assign_collector.html', {'pickup': pickup, 'collectors': collectors})

# Update pickup status — admin
@login_required
@user_passes_test(admin_required)
def update_status(request, pickup_id):
    pickup = get_object_or_404(PickupRequest, id=pickup_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(PickupRequest.STATUS_CHOICES):
            pickup.status = status
            pickup.save()
            messages.success(request, f'Status updated for pickup request #{pickup.id}.')
        else:
            messages.error(request, 'Invalid status selected.')
    return redirect('ecotracksys:pickup_management')

# Reschedule pickup (admin modal handler)
@login_required
@user_passes_test(admin_required)
def reschedule_pickup(request, pickup_id):
    pickup = get_object_or_404(PickupRequest, id=pickup_id)

    if request.method == "POST":
        # Match the form field names in your modal
        new_date = request.POST.get("new_date")
        new_time = request.POST.get("new_time")

        if new_date and new_time:
            try:
                # Parse new values
                pickup.pickup_date = parse_date(new_date)
                pickup.pickup_time = datetime.strptime(new_time, "%H:%M").time()

                # If still pending, keep it pending, else ensure it goes back to In Progress
                if pickup.status == "Completed":
                    messages.warning(request, "Completed requests cannot be rescheduled.")
                else:
                    pickup.status = "In Progress"
                    pickup.save()
                    messages.success(request, f"Pickup request {pickup.id} rescheduled successfully.")
            except Exception as e:
                messages.error(request, f"Invalid date/time format: {e}")
        else:
            messages.error(request, "Both date and time are required.")

    return redirect("ecotracksys:pickup_management")

# Zone route management (staff-only)
@staff_member_required
def zone_management(request):
    if request.method == "POST":
        zone_name = request.POST.get("zone_name")
        ward = request.POST.get("ward", "")
        lat_min = float(request.POST.get("lat_min", 0))
        lat_max = float(request.POST.get("lat_max", 0))
        lng_min = float(request.POST.get("lng_min", 0))
        lng_max = float(request.POST.get("lng_max", 0))

        if Zone.objects.filter(name=zone_name).exists():
            messages.error(request, "Zone already exists!")
            return redirect('zone_management')

        Zone.objects.create(
            name=zone_name,
            ward=ward,
            lat_min=lat_min,
            lat_max=lat_max,
            lng_min=lng_min,
            lng_max=lng_max
        )
        messages.success(request, "Zone added successfully!")
        return redirect('zone_management')

    zones = Zone.objects.all()
    return render(request, "ecotracksys/admin_dashboard/zone_route_management.html", {"zones": zones})


# ============================================================
# 6. COLLECTOR DASHBOARD & MANAGEMENT
# ============================================================

# Note: is_admin is redefined in multiple places in the original file — duplicated intentionally
def is_admin(user):
    return user.is_authenticated and user.role == "admin"

# Collector pickup history (note: original code references Pickup model — kept as-is)
@login_required
def pickup_history(request):
    user = request.user
    if user.role != 'collector':  # ensure only collectors access this
        return redirect('ecotracksys:dashboard_home')  # or any other safe page

    # Your existing code to fetch pickup history
    pickups = Pickup.objects.filter(collector=user).order_by('-pickup_date')
    
    context = {
        'pickups': pickups,
    }
    return render(request, 'collector_dashboard/collector_pickup_history.html', {'pickups': pickups})

# Collector leave request page
@login_required
def collector_leave_request(request):
    leaves = LeaveRequest.objects.filter(collector=request.user)
    return render(request, 'collector_dashboard/collector_leave_request.html', {'leaves': leaves})

# Collector settings page
@login_required
def collector_settings(request):
    return render(request, 'collector_dashboard/collector_settings.html')

# Collector management (admin creates collectors)
@login_required
def collector_management(request):
    if request.method == "POST":
        name = request.POST.get("collector_name")
        email = request.POST.get("collector_email")
        phone = request.POST.get("collector_phone")
        zone_name = request.POST.get("collector_zone")
        password = request.POST.get("collector_password")

        # get or create zone if necessary
        zone, _ = Zone.objects.get_or_create(name=zone_name)

        # Create collector
        try:
            collector = CustomUser.objects.create(
                name=name,
                email=email,
                phone=phone,
                role="collector",
                zone=zone,
                password=make_password(password)  # hash the password
            )
            messages.success(request, "Collector added successfully.")
        except Exception as e:
            messages.error(request, f"Error creating collector: {str(e)}")

        return redirect("ecotracksys:collector_management")

    # GET request → list collectors
    collectors = CustomUser.objects.filter(role="collector")
    return render(request, "ecotracksys/admin_dashboard/collector_management.html", {
        "collectors": collectors
    })

# Edit collector (admin)
@login_required
@user_passes_test(is_admin)
def edit_collector(request, pk):
    collector = get_object_or_404(CustomUser, pk=pk, role='collector')
    if request.method == 'POST':
        collector.name = request.POST.get('collector_name')
        collector.email = request.POST.get('collector_email')
        collector.phone = request.POST.get('collector_phone')
        collector.zone = request.POST.get('collector_zone')
        password = request.POST.get('collector_password')
        if password:
            collector.set_password(password)
        collector.save()
        messages.success(request, "Collector updated successfully!")
        return redirect('collector_management')
    return render(request, 'ecotracksys/admin_dashboard/edit_collector.html', {'collector': collector})

# Toggle collector active/inactive (admin AJAX)
@login_required
@user_passes_test(is_admin)
@require_POST
def toggle_collector_status(request, collector_id):
    try:
        collector = CustomUser.objects.get(id=collector_id, role='collector')
        collector.status = 'Inactive' if collector.status == 'Active' else 'Active'
        collector.save()
        return JsonResponse({'success': True, 'status': collector.status})
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Collector not found'})

# Delete collector (admin)
@login_required
@user_passes_test(is_admin)
def collector_delete(request, pk):
    collector = get_object_or_404(CustomUser, id=pk, role='collector')
    collector.delete()
    messages.success(request, "Collector deleted successfully.")
    return redirect("collector_management")


# ============================================================
# 7. USER / ADMIN MANAGEMENT
# ============================================================

@staff_member_required
def user_management(request):
    admins = CustomUser.objects.filter(role='admin')
    users = CustomUser.objects.filter(role='citizen')

    if request.method == 'POST':
        if request.POST.get('role') == 'admin':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "An admin with this email already exists.")
            else:
                CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    name=name,
                    role='admin',
                    is_staff=True,
                    is_superuser=True
                )
                messages.success(request, f"Admin {name} created successfully.")
                return redirect('user_management')

    context = {'admins': admins, 'users': users}
    return render(request, 'ecotracksys/admin_dashboard/user_management.html', context)

@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, "User updated successfully!")
        return redirect('user_management')
    return render(request, 'ecotracksys/admin_dashboard/edit_user.html', {'user': user})

def edit_user_inline(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, "User updated successfully!")
        return redirect('user_management')
    return render(request, 'ecotracksys/admin_dashboard/edit_user_inline.html', {'user': user})

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully!")
    return redirect('user_management')


# ============================================================
# 8. COMPLAINT MANAGEMENT
# ============================================================

@staff_member_required
def complaint_management(request):
    complaints = Complaint.objects.all().order_by('-date_submitted')
    return render(request, 'ecotracksys/admin_dashboard/complaint_management.html', {'complaints': complaints})

@staff_member_required
def update_complaint_status(request):
    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        status = request.POST.get("status")
        note = request.POST.get("note", "")
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.status = status
        complaint.notes = note
        complaint.save()
    return redirect('complaint_management')

@staff_member_required
def delete_complaint(request):
    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.delete()
    return redirect('complaint_management')


# ============================================================
# 9. LEAVE REQUEST MANAGEMENT
# ============================================================

@staff_member_required
def leave_request_management(request):
    leave_requests = LeaveRequest.objects.all().order_by('-created_at')
    return render(request, 'ecotracksys/admin_dashboard/leave_req_management.html', {'leave_requests': leave_requests})


# ============================================================
# 10. SYSTEM SETTINGS & ANALYTICS
# ============================================================

@staff_member_required
def analytics(request):
    pickup_data = [120, 150, 180, 200, 220, 250]
    user_data = [50, 70, 90, 120, 140, 160]
    return render(request, 'ecotracksys/admin_dashboard/analytics.html', {'pickup_data': pickup_data, 'user_data': user_data})

@staff_member_required
def admin_profile(request):
    return render(request, 'ecotracksys/admin_dashboard/admin_profile.html')


# -----------------------------------------------------------------
# Additional zone-form view (kept as in original)
# -----------------------------------------------------------------
from django.shortcuts import render, redirect
from .forms import ZoneForm

def add_zone(request):
    if request.method == "POST":
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zone_management')  # redirect to your zone management page
    else:
        form = ZoneForm()
    return render(request, 'admin_dashboard/add_zone.html', {'form': form})

# ============================================================
# Collector Dashboard (another block from original file)
# ============================================================
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import PickupRequest

# Collector dashboard — shows today's assignments and metrics
@login_required
def collector_dashboard(request):
    user = request.user
    if user.role != 'collector':
        return redirect('home')  # redirect if not collector

    today = timezone.localdate()
    todays_assignments = PickupRequest.objects.filter(
        collector=user,
        pickup_date=today
    )

    context = {
        'tasks_today': todays_assignments.count(),
        'tasks_completed_today': todays_assignments.filter(status='done').count(),
        'tasks_pending_today': todays_assignments.filter(status='assigned').count(),
        'tasks_missed_today': todays_assignments.filter(status='missed').count(),
        'todays_assignments': todays_assignments,
        'zones': PickupRequest.objects.values_list('pickup_time_slot', flat=True).distinct(),
        'notifications': [],
        'trend_last_7': [3, 4, 5, 2, 6, 4, 5],
        'shift_active': False,
        'last_synced': timezone.now(),
    }
    return render(request, 'ecotracksys/collector_dashboard/collector_dashboard.html', context)

# ====================================
# Collector — helper and views (more duplicates preserved)
# ====================================
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Helper: check if user is collector
def is_collector(user):
    return user.is_authenticated and user.role == 'collector'

# Performance report for collectors
@login_required
@user_passes_test(is_collector)
def collector_performance(request):
    """Performance report page for collectors."""
    return render(request, 'ecotracksys/collector_dashboard/performance_report.html')

# Collector leave planner + history
@login_required
@user_passes_test(is_collector)
def collector_leave(request):
    """Leave request + leave history page for collectors."""
    return render(request, 'ecotracksys/collector_dashboard/leave_planner.html')

# Collector notifications page
@login_required
@user_passes_test(is_collector)
def collector_notifications(request):
    """Notifications page for collectors."""
    return render(request, 'ecotracksys/collector_dashboard/notifications.html')

# Collector-facing complaints view
@login_required
@user_passes_test(is_collector)
def collector_complaints(request):
    """Complaints page for collectors."""
    return render(request, 'ecotracksys/collector_dashboard/complaints.html')

# Collector profile (view + update) — POST updates name/phone/image
def collector_profile(request):
    """
    Display and update collector profile.
    GET: Show profile form with current user info.
    POST: Update name, phone, and profile image.
"""
    user = request.user

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        profile_image = request.FILES.get("profile_image")

        # Update fields
        user.name = name
        user.phone = phone
        if profile_image:
            user.profile_image = profile_image

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("ecotracksys:collector_profile")
    return render(request, 'ecotracksys/collector_dashboard/collector_profile.html')

# Mark a notification read (collector/citizen)
def mark_notification_read(request):
    if request.method == 'POST':
        notif_id = request.POST.get('notif_id')
        try:
            notif = Notification.objects.get(id=notif_id, user=request.user)
            notif.status = 'read'
            notif.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# Mark a notification unread
def mark_notification_unread(request):
    if request.method == 'POST':
        notif_id = request.POST.get('notif_id')
        try:
            notif = Notification.objects.get(id=notif_id, user=request.user)
            notif.status = 'unread'
            notif.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# Delete a notification
def delete_notification(request):
    if request.method == 'POST':
        notif_id = request.POST.get('notif_id')
        try:
            notif = Notification.objects.get(id=notif_id, user=request.user)
            notif.delete()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# -----------------------------
# Assign collector (duplicate occurrence kept)
# -----------------------------
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

@login_required
@user_passes_test(admin_required)
def assign_collector(request, pickup_id):
    pickup = get_object_or_404(PickupRequest, id=pickup_id)
    if request.method == 'POST':
        collector_id = request.POST.get('collector_id')
        if collector_id:
            collector = get_object_or_404(CustomUser, id=collector_id, role='collector')
            pickup.collector = collector
            pickup.status = 'In Progress'  # better than 'Assigned'
            pickup.save()
            collector_name = collector.name or collector.email
            messages.success(request, f'Collector {collector_name} assigned to pickup request #{pickup.id}.')
        else:
            messages.error(request, 'Please select a collector.')
    return redirect('ecotracksys:pickup_management')

# Admin reschedule pickup (similar to earlier reschedule view — kept)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from ecotracksys.models import PickupRequest

@staff_member_required
def admin_reschedule_pickup(request, pickup_id):
    pickup = get_object_or_404(PickupRequest, id=pickup_id)
    if request.method == 'POST':
        pickup.pickup_date = request.POST.get('new_date')
        pickup.pickup_time = request.POST.get('new_time')
        pickup.status = 'Pending'  # Optional: reset status
        pickup.save()
    return redirect('ecotracksys:pickup_management')

# -----------------------------
# JSON / API style pickup details (admin)
# -----------------------------
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404

# ✅ Adjust this import to where your model lives
from ecotracksys.models import PickupRequest  # or: from ecotracksys.models import PickupRequest
from accounts.models import CustomUser  # your custom user with role field

# is_admin defined again (duplicate kept)
def is_admin(user):
    # Tailor to your logic; many projects use user.is_staff or a 'role' field.
    return user.is_authenticated and (getattr(user, "role", "") == "admin" or user.is_staff)

# Return JSON details about a pickup (admin only)
@require_GET
@login_required
@user_passes_test(is_admin)
def pickup_details_json(request, pk):
    pickup = get_object_or_404(PickupRequest, pk=pk)

    # Limit to active collectors
    collectors_qs = CustomUser.objects.filter(role="collector", is_active=True).values("id", "email")

    data = {
        "id": pickup.id,
        "customer_name": pickup.customer_name or "",
        "pickup_date": pickup.pickup_date.strftime("%Y-%m-%d") if pickup.pickup_date else "",
        "pickup_time": pickup.pickup_time.strftime("%H:%M") if pickup.pickup_time else "",
        "address": pickup.address or "",
        "status": pickup.status or "Pending",
        "collector_id": pickup.collector_id if getattr(pickup, "collector_id", None) else None,
        "collectors": list(collectors_qs),
    }
    return JsonResponse(data)

# -----------------------------
# Collector dashboard (another duplicate block)
# -----------------------------
@login_required
def collector_dashboard(request):
    collector = request.user
    today = timezone.now().date()

    tasks = PickupRequest.objects.filter(collector=collector, pickup_date=today)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status=PickupRequest.STATUS_COMPLETED).count()
    pending_tasks = tasks.filter(status=PickupRequest.STATUS_PENDING).count()
    missed_tasks = tasks.filter(status=PickupRequest.STATUS_CANCELLED).count()

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'missed_tasks': missed_tasks,
    }
    return render(request, 'collector_dashboard/collector_dashboard.html', context)

# is_collector defined again (duplicate kept)
def is_collector(user):
    return user.role == 'collector'

# -----------------------------
# Collector Assignments and history
# -----------------------------
# Note: multiple duplicates kept as in original file
@login_required
@user_passes_test(is_collector)
@login_required
@user_passes_test(is_collector)
def collector_assignments(request):
    collector = request.user
    assignments = PickupRequest.objects.filter(collector=collector).order_by('-pickup_date', 'pickup_time')

    print("Assignments for", collector.email)
    for a in assignments:
        print(a.id, a.status, a.pickup_date)

    return render(request, 'collector_dashboard/my_assignments.html', {'assignments': assignments})

# Collector pickup history
@login_required
def collector_pickup_history(request):
    collector = request.user
    history = PickupRequest.objects.filter(collector=collector)
    return render(request, 'collector_dashboard/collector_pickup_history.html', {'history': history})

# Collector dashboard duplicate block — preserved
@login_required
def collector_dashboard(request):
    collector = request.user
    today = timezone.now().date()

    tasks = PickupRequest.objects.filter(collector=collector, pickup_date=today)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status=PickupRequest.STATUS_COMPLETED).count()
    pending_tasks = tasks.filter(status=PickupRequest.STATUS_PENDING).count()
    missed_tasks = tasks.filter(status=PickupRequest.STATUS_CANCELLED).count()

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'missed_tasks': missed_tasks,
    }
    return render(request, 'ecotracksys/collector_dashboard/collector_dashboard.html', context)

# Another collector assignments view (duplicate, renders different template name)
@login_required
def collector_assignments(request):
    collector = request.user
    today = timezone.now().date()
    assignments = PickupRequest.objects.filter(
        collector=collector,
        pickup_date=today
    )

    # Debug prints
    print("Logged-in collector:", collector)
    print("Assignments queryset:", assignments)
    return render(request, 'collector_dashboard/my_assignment.html', {'assignments': assignments})

# Another collector pickup history duplicate — different template path
@login_required
def collector_pickup_history(request):
    collector = request.user
    history = PickupRequest.objects.filter(collector=collector)
    return render(request, 'ecotracksys/collector_dashboard/pickup_history.html', {'history': history})

# ============================================================
# ZONE MANAGEMENT VIEWS (additional duplicates preserved)
# ============================================================
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Zone
from accounts.models import CustomUser  # ensure you import your custom user

# check if user is admin (redefinition kept)
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# Zone management landing (admin-only)
@login_required
@user_passes_test(is_admin)
def zone_management(request):
    zones = Zone.objects.all()
    collectors = CustomUser.objects.filter(role='collector')
    return render(request, "ecotracksys/admin_dashboard/zone_route_management.html", {
        "zones": zones,
        "collectors": collectors
    })

# Add zone (admin)
@login_required
@user_passes_test(is_admin)
def add_zone(request):
    if request.method == "POST":
        name = request.POST.get("name")
        ward = request.POST.get("ward")
        Zone.objects.create(name=name, ward=ward)
        messages.success(request, "Zone added successfully!")
        return redirect("zone_management")
    return redirect("zone_management")

# Edit zone (admin)
@login_required
@user_passes_test(is_admin)
def edit_zone(request, zone_id):
    zone = get_object_or_404(Zone, id=zone_id)
    if request.method == "POST":
        zone.name = request.POST.get("name")
        zone.ward = request.POST.get("ward")
        zone.save()
        messages.success(request, "Zone updated successfully!")
        return redirect("ecotracksys:zone_management")
    return redirect("ecotracksys:zone_management")

# Delete zone (admin)
@login_required
@user_passes_test(is_admin)

def delete_zone(request, zone_id):
    zone = get_object_or_404(Zone, id=zone_id)  # safer than Zone.objects.get()
    if request.method == "POST":
        zone.delete()
        messages.success(request, f"Zone '{zone.name}' deleted successfully.")
        return redirect("ecotracksys:zone_management")
    return redirect("ecotracksys:zone_management")

# Assign collector to a zone (admin)
@login_required
@user_passes_test(is_admin)
def assign_collector(request, zone_id):
    zone = get_object_or_404(Zone, id=zone_id)
    if request.method == "POST":
        collector_id = request.POST.get("collector")
        collector = CustomUser.objects.filter(id=collector_id, role="collector").first()
        if collector:
            zone.collector = collector
            zone.save()
            messages.success(request, f"Collector {collector.email} assigned successfully!")
    return redirect("ecotracksys:zone_management")
