from .models import Issue   # if Issue is inside the same app’s models.py
from datetime import timedelta
from django.http import JsonResponse
from urllib import request
from django.contrib.auth.decorators import login_required
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
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import CollectorShift
# Landing page — public
from django.shortcuts import render
from accounts.models import CustomUser
from .models import PickupRequest
def home(request):
    completed_pickups = PickupRequest.objects.filter(status="completed").count()
    active_users = CustomUser.objects.filter(role="citizen", is_active=True).count()
    active_collectors = CustomUser.objects.filter(role="collector", is_active=True).count()
    return render(request, "ecotracksys/landing_page/index.html", {
        "completed_pickups": completed_pickups,
        "active_users": active_users,
        "active_collectors": active_collectors,
    })
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
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PickupRequest
@login_required
def citizen_dashboard(request):
    user = request.user
    today = timezone.localdate()   # today's date
    # === Counts ===
    total_pickups_count = PickupRequest.objects.filter(user=user).count()
    pending_requests_count = PickupRequest.objects.filter(
        user=user,
        status=PickupRequest.STATUS_PENDING
    ).count()
    # upcoming = all pickups scheduled today or later, not yet completed
    upcoming_pickups_count = PickupRequest.objects.filter(
    user=user,
    pickup_date=today,  # only today
    status=PickupRequest.STATUS_IN_PROGRESS  # only assigned ones
).count()
    latest_requests = PickupRequest.objects.filter(user=request.user).order_by( '-pickup_date', '-pickup_time')[:10]
    context = {
        'total_pickups_count': total_pickups_count,
        'pending_requests_count': pending_requests_count,
        'upcoming_pickups_count': upcoming_pickups_count,
    }
    return render(request, 'ecotracksys/user_dashboard/index.html', context)
# Citizen profile view — requires login
@login_required
def citizen_profile(request):
    return render(request, 'ecotracksys/user_dashboard/my_profile.html')

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
# views.py
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PickupRequest
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
        pickup_date_str = request.POST.get("pickup_date")
        pickup_time_from_str = request.POST.get("pickup_time_from")  # "09:30 AM"
        pickup_time_to_str = request.POST.get("pickup_time_to")      # "11:00 AM"
        quantity = request.POST.get("quantity") or 1
        special_instructions = request.POST.get("special_instructions", "")
        # ----------- Validate pickup date -----------
        if not pickup_date_str:
            messages.error(request, "❌ Please select a pickup date.")
            return redirect('ecotracksys:citizen_pickup_request')
        try:
            pickup_date = datetime.strptime(pickup_date_str, "%d-%m-%y").date()
        except ValueError:
            messages.error(request, "❌ Invalid pickup date format.")
            return redirect('ecotracksys:citizen_pickup_request')
        # ----------- Validate pickup times (12-hour format) -----------
        if not pickup_time_from_str or not pickup_time_to_str:
            messages.error(request, "❌ Please select both pickup times.")
            return redirect('ecotracksys:citizen_pickup_request')
        try:
            pickup_time_from = datetime.strptime(pickup_time_from_str, "%I:%M %p").time()
            pickup_time_to = datetime.strptime(pickup_time_to_str, "%I:%M %p").time()
        except ValueError:
            messages.error(request, "❌ Invalid time format.")
            return redirect('ecotracksys:citizen_pickup_request')
        if pickup_time_from >= pickup_time_to:
            messages.error(request, '❌ "From" time must be earlier than "To" time.')
            return redirect('ecotracksys:citizen_pickup_request')
        # ----------- Validate location -----------
        if not lat or not lng:
            messages.error(request, '❌ Please select a location on the map.')
            return redirect('ecotracksys:citizen_pickup_request')
        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            messages.error(request, '❌ Invalid latitude or longitude.')
            return redirect('ecotracksys:citizen_pickup_request')
        # ----------- Create PickupRequest -----------
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
            pickup_time=pickup_time_from,  # store start time
            pickup_time_slot=f"{pickup_time_from_str} - {pickup_time_to_str}",  # human-readable
            quantity=int(quantity),
            special_instructions=special_instructions
        )
        messages.success(request, "✅ Pickup request created successfully!")
        return redirect('ecotracksys:citizen_pickup_request')
    # -------- GET request -----------
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
         # ✅ handle profile image update
        if request.FILES.get("profile_image"):
            request.user.profile_image = request.FILES["profile_image"]
            print("Uploaded file:", request.FILES.get("profile_image"))
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
            return redirect('ecotracksys:user_dashboard')
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
# views.py
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from datetime import datetime
@login_required
@user_passes_test(admin_required)
def reschedule_pickup(request, pickup_id):
    pickup = get_object_or_404(PickupRequest, id=pickup_id)
    if request.method == "POST":
        new_date = request.POST.get("new_date")
        new_time = request.POST.get("new_time")
        if new_date and new_time:
            try:
                pickup.pickup_date = parse_date(new_date)
                pickup.pickup_time = datetime.strptime(new_time, "%H:%M").time()
                if pickup.status in ["Completed", "Cancelled"]:
                    return JsonResponse({
                        "success": False,
                        "message": f"{pickup.status} requests cannot be rescheduled."
                    })
                pickup.status = "Pending"   # keep it pending after reschedule
                pickup.save()
                return JsonResponse({
                    "success": True,
                    "message": f"Pickup {pickup.id} rescheduled successfully.",
                    "new_date": pickup.pickup_date.strftime("%Y-%m-%d"),
                    "new_time": pickup.pickup_time.strftime("%H:%M"),
                    "status": pickup.status
                })
            except Exception as e:
                return JsonResponse({"success": False, "message": f"Invalid date/time: {e}"})
        else:
            return JsonResponse({"success": False, "message": "Both date and time are required."})
    return JsonResponse({"success": False, "message": "Invalid request."})
# Zone route management (staff-only)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# ============================================================
# 6. COLLECTOR DASHBOARD & MANAGEMENT
# ============================================================
# Note: is_admin is redefined in multiple places in the original file — duplicated intentionally
def is_admin(user):
    return user.is_authenticated and user.role == "admin"
# Collector pickup history (note: original code references Pickup model — kept as-is)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PickupRequest
@login_required
def collector_pickup_history(request):
    # Get pickups for this collector with specific statuses only
    pickups = PickupRequest.objects.filter(
        assigned_collector=request.user,
        status__in=["Completed", "Missed", "Cancelled"]  # include only these statuses
    ).order_by("-pickup_date", "-pickup_time").select_related("user")
    return render(request, "ecotracksys/collector_dashboard/pickup_history.html", {"pickups": pickups})
# Collector leave request page
# ecotracksys/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import LeaveRequest
# Check if user is a collector
def is_collector(user):
    return user.is_authenticated and user.role == 'collector'
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import LeaveRequest
from datetime import datetime
@login_required
def collector_leave(request):
    """
    Display leave form and leave history, handle new leave requests.
    """
    # Pre-fill form values
    form_data = {'leave_type':'', 'start_date':'', 'end_date':'', 'reason':''}
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        reason = request.POST.get('reason')
        form_data = {
            'leave_type': leave_type,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'reason': reason
        }
        # Basic validation
        if not all([leave_type, start_date_str, end_date_str, reason]):
            messages.error(request, "All fields are required.")
        else:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                today = timezone.now().date()
                if start_date < today:
                    messages.error(request, "Start date cannot be in the past.")
                elif start_date > end_date:
                    messages.error(request, "End date must be the same as or after start date.")
                else:
                    # Check overlapping leaves
                    overlapping = LeaveRequest.objects.filter(
                        collector=request.user,
                        status__in=['Pending', 'Approved'],
                        start_date__lte=end_date,
                        end_date__gte=start_date
                    )
                    if overlapping.exists():
                        messages.error(request, "You already have a leave request overlapping these dates.")
                    else:
                        # ✅ Ensure leave_type is a valid choice before saving
                        if leave_type not in dict(LeaveRequest.LEAVE_TYPE_CHOICES):
                            messages.error(request, "Invalid leave type selected.")
                        else:
                            # Save leave
                            leave = LeaveRequest(
                                collector=request.user,
                                leave_type=leave_type,
                                start_date=start_date,
                                end_date=end_date,
                                reason=reason,
                                status='Pending'
                            )
                            leave.save()
                            messages.success(request, "Leave request submitted successfully!")
                            form_data = {'leave_type':'', 'start_date':'', 'end_date':'', 'reason':''}
            except ValueError:
                messages.error(request, "Invalid date format.")
    # Fetch leave history
    leaves = LeaveRequest.objects.filter(collector=request.user).order_by('-applied_at')
    context = {
        'leaves': leaves,
        'form_data': form_data
    }
    return render(request, 'ecotracksys/collector_dashboard/leave_planner.html', context)
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.contrib.auth.decorators import login_required
# Collector management (admin creates collectors)
@login_required
def collector_management(request):
    if request.method == "POST":
        name = request.POST.get("collector_name")
        email = request.POST.get("collector_email")
        phone = request.POST.get("collector_phone")
        raw_password = request.POST.get("collector_password")  # keep raw password
        # Create collector
        try:
            collector = CustomUser.objects.create(
                name=name,
                email=email,
                phone=phone,
                role="collector",
                password=make_password(raw_password)  # hash the password
            )
            # ----------------- Send email -----------------
            subject = "Your EcoTrack Collector Account"
            message = f"""
Hello {collector.name},
Your account has been created in EcoTrack.
Login details:
Email: {collector.email}
Password: {raw_password}
Please log in and change your password after first login.
"""
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [collector.email]
            send_mail(subject, message, from_email, recipient_list)
            # ----------------- Email sent -----------------
            messages.success(request, "Collector added successfully and email sent.")
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
    return redirect('ecotracksys:complaint_management')
@staff_member_required
def delete_complaint(request,complaint_id):
    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.delete()
    return redirect('ecotracksys:complaint_management')
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
from django.db.models import Count
def admin_analytics(request):
    # KPI counts
    total_pickups = PickupRequest.objects.count()
    completed_pickups = PickupRequest.objects.filter(status='Completed').count()
    pending_pickups = PickupRequest.objects.filter(status='Pending').count()
    total_collectors = CustomUser.objects.filter(role='collector').count()
    # Pickup status distribution for pie chart
    status_data = PickupRequest.objects.values('status').annotate(count=Count('id'))
    context = {
        'total_pickups': total_pickups,
        'completed_pickups': completed_pickups,
        'pending_pickups': pending_pickups,
        'total_collectors': total_collectors,
        'status_data': list(status_data),  # Convert queryset to list for template
    }
    return render(request, 'ecotracksys/admin_dashboard/analytics.html', context)
from django.shortcuts import render, redirect
from .forms import AdminProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AdminProfileForm  # make sure this form exists
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import AdminProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import AdminProfileForm
@login_required
def admin_profile(request):
    user = request.user
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save(request=request)  # pass request here
            messages.success(request, "Profile updated successfully!")
            return redirect('ecotracksys:admin_profile')
    else:
        form = AdminProfileForm(instance=user)
    activity_log = [
        {'icon': 'bi-clock-history', 'desc': 'Logged in on 1 Aug 2025 at 9:00 AM'},
        {'icon': 'bi-person-check', 'desc': 'Assigned pickup to Collector #23'},
        {'icon': 'bi-geo-alt-fill', 'desc': 'Updated zone details for Sector-17'},
        {'icon': 'bi-check-circle', 'desc': 'Reviewed leave request of Collector #11'},
    ]
    return render(request, 'ecotracksys/admin_dashboard/admin_profile.html', {
        'form': form,
        'activity_log': activity_log
    })
# ecotracksys/views.py
from django.shortcuts import render
from django.db.models import Count, Avg, F
from accounts.models import CustomUser
from .models import PickupRequest
import json
from django.db.models.functions import TruncMonth
def analytics_view(request):
    # -------- Pickup Status Distribution --------
    status_qs = PickupRequest.objects.values('status').annotate(count=Count('id'))
    status_labels = [entry['status'] for entry in status_qs]
    status_counts = [entry['count'] for entry in status_qs]
    # -------- Pickup Trends Over Time (Monthly) --------
    trends_qs = PickupRequest.objects.annotate(month=TruncMonth('pickup_date')).values('month').annotate(count=Count('id')).order_by('month')
    trends_labels = [entry['month'].strftime('%b %Y') for entry in trends_qs]
    trends_counts = [entry['count'] for entry in trends_qs]
    # -------- Collector Performance --------
    collectors = CustomUser.objects.filter(role='collector')
    collector_labels = [c.get_full_name() or c.email for c in collectors]
    collector_assigned = []
    collector_completed = []
    for c in collectors:
        assigned = PickupRequest.objects.filter(collector=c).count()
        completed = PickupRequest.objects.filter(collector=c, status='Completed').count()
        collector_assigned.append(assigned)
        completion_rate = round((completed/assigned)*100, 2) if assigned > 0 else 0
        collector_completed.append(completion_rate)
    # -------- Citizen Activity --------
    citizens = CustomUser.objects.filter(role='citizen')
    citizen_labels = [c.get_full_name() or c.email for c in citizens]
    citizen_requests = [PickupRequest.objects.filter(user=c).count() for c in citizens]
    # -------- Waste Type Distribution (Optional) --------
    waste_types = PickupRequest.objects.values('waste_type').annotate(count=Count('id'))
    waste_labels = [entry['waste_type'] for entry in waste_types]
    waste_counts = [entry['count'] for entry in waste_types]
    context = {
        'status_labels': json.dumps(status_labels),
        'status_counts': json.dumps(status_counts),
        'trends_labels': json.dumps(trends_labels),
        'trends_counts': json.dumps(trends_counts),
        'collector_labels': json.dumps(collector_labels),
        'collector_assigned': json.dumps(collector_assigned),
        'collector_completed': json.dumps(collector_completed),
        'citizen_labels': json.dumps(citizen_labels),
        'citizen_requests': json.dumps(citizen_requests),
        'waste_labels': json.dumps(waste_labels),
        'waste_counts': json.dumps(waste_counts),
    }
    return render(request, 'ecotracksys/admin_dashboard/analytics.html', context)
# ============================================================
# Collector Dashboard (another block from original file)
# ============================================================
# ecotracksys/views.py
from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .models import PickupRequest  # assumes your model is here
@login_required
def collector_dashboard(request):
    # only collectors allowed
    if getattr(request.user, "role", None) != "collector":
        return render(request, "403.html", status=403)
    # use local date (timezone-aware)
    today = timezone.localdate()
    # Today's assignments for this collector
    todays_assignments = PickupRequest.objects.filter(
        collector=request.user,
        scheduled_date=today
    ).order_by("scheduled_time")
    # Robust, case-insensitive status checks — adjust these if your DB uses different strings
    done_q = Q(status__iexact="done") | Q(status__iexact="completed")
    missed_q = Q(status__iexact="missed") | Q(status__iexact="missed_pickup")
    tasks_today = todays_assignments.count()
    tasks_completed_today = todays_assignments.filter(done_q).count()
    tasks_missed = todays_assignments.filter(missed_q).count()
    # Pending = anything assigned for today that is not completed/missed.
    tasks_pending = tasks_today - tasks_completed_today - tasks_missed
    if tasks_pending < 0:
        tasks_pending = 0
    # Notifications: optional model. Fallback to empty list if model isn't present.
    notifications = []
    try:
        from .models import Notification  # optional
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:6]
    except Exception:
        notifications = []
    # shift_active: try Shift model first; otherwise fall back to session flag
    shift_active = request.session.get("shift_active", False)
    try:
        from .models import Shift  # optional Shift model
        # example: active shift is one with no end_time
        shift_active = Shift.objects.filter(collector=request.user, end_time__isnull=True).exists()
    except Exception:
        # keep session-based value as fallback
        pass
    # Performance: build a simple 7-day series (useful for charts)
    start_date = today - timedelta(days=6)
    performance = []
    for i in range(7):
        d = start_date + timedelta(days=i)
        total = PickupRequest.objects.filter(collector=request.user, scheduled_date=d).count()
        completed = PickupRequest.objects.filter(collector=request.user, scheduled_date=d).filter(done_q).count()
        performance.append({
            "date": d.isoformat(),
            "total": total,
            "completed": completed,
        })
    context = {
        "todays_assignments": todays_assignments,
        "tasks_today": tasks_today,
        "tasks_completed_today": tasks_completed_today,
        "tasks_pending": tasks_pending,
        "tasks_missed": tasks_missed,
        "notifications": notifications,
        "shift_active": shift_active,
        "performance": performance,
    }
    return render(request, "ecotracksys/collector_dashboard/collector_dashboard.html", context)
# ====================================
# Collector — helper and views (more duplicates preserved)
# ====================================
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
# Helper: check if user is collector
def is_collector(user):
    return user.is_authenticated and user.role == 'collector'
# Performance report for collectors
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, localdate
from datetime import timedelta
from collections import Counter
from .models import PickupRequest  # adjust import to your app
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localdate
from collections import Counter
from datetime import timedelta
from .models import PickupRequest
@login_required
def collector_performance(request):
    collector = request.user
    # All pickups assigned to collector
    pickups = PickupRequest.objects.filter(collector=collector)
    # KPIs
    total_pickups = pickups.exclude(status="Pending").count()  # exclude pending for history
    completed_pickups = pickups.filter(status="Completed").count()
    missed_pickups = pickups.filter(status="Missed").count()
    efficiency = f"{(completed_pickups / total_pickups * 100):.1f}%" if total_pickups > 0 else "0%"
    # Weekly completed pickups trend
    today = localdate()
    last_week = today - timedelta(days=6)
    daily_counts = []
    labels = []
    for i in range(7):
        day = last_week + timedelta(days=i)
        labels.append(day.strftime("%a"))
        daily_counts.append(pickups.filter(status="Completed", pickup_date=day).count())
    # Waste breakdown (include both Completed and Missed)
    waste_data = pickups.exclude(status="Pending").values_list("waste_type", flat=True)
    counter = Counter(waste_data)
    waste_types = list(counter.keys()) if counter else ["Organic", "Plastic", "Paper", "Metal"]
    waste_counts = list(counter.values()) if counter else [0, 0, 0, 0]
    context = {
        "total_pickups": total_pickups,
        "completed_pickups": completed_pickups,
        "missed_pickups": missed_pickups,
        "efficiency": efficiency,
        "weekly_data": daily_counts,
        "waste_types": waste_types,
        "waste_counts": waste_counts,
    }
    return render(request, "ecotracksys/collector_dashboard/performance_report.html", context)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
@login_required
def collector_notifications(request):
    # Ensure only collectors can access
    if request.user.role != 'collector':
        return render(request, "403.html", status=403)
    # Fetch notifications for this collector, newest first (model ordering already does this)
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'ecotracksys/collector_dashboard/notifications.html', {
        'notifications': notifications
    })
# Collector-facing complaints view
@login_required
@user_passes_test(is_collector)
def collector_complaints(request):
    """Complaints page for collectors."""
    return render(request, 'ecotracksys/collector_dashboard/complaints.html')
# Collector profile (view + update) — POST updates name/phone/image
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm  # make sure this form has name, phone, profile_image
from .forms import CollectorProfileForm
@login_required
def collector_profile(request):
    user = request.user
    if request.method == "POST":
        form = CollectorProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, "Profile updated successfully!")
            return redirect("ecotracksys:collector_profile")
    else:
        form = CollectorProfileForm(instance=user)
    return render(request, 'ecotracksys/collector_dashboard/collector_profile.html', {'form': form})
# -----------------------------
# Assign collector 
# -----------------------------
import random
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import PickupRequest, CustomUser
def assign_collector(request, pickup_id):
    if request.method == 'POST':
        pickup = get_object_or_404(PickupRequest, id=pickup_id)
        collector_id = request.POST.get('collector_id')
        if collector_id:
            collector = get_object_or_404(CustomUser, id=collector_id, role='collector')
            # Assign collector
            pickup.assigned_collector = collector
            pickup.status = 'In Progress'  # better than 'Assigned'
            # Generate 6-digit OTP
            pickup.otp = f"{random.randint(100000, 999999)}"
            pickup.save()
            collector_name = collector.full_name or collector.email
            messages.success(
                request, 
                f'Collector {collector_name} assigned to pickup request #{pickup.id}. OTP: {pickup.otp}'
            )
        else:
            messages.error(request, 'Please select a collector.')   
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
# is_collector defined again (duplicate kept)
def is_collector(user):
    return user.role == 'collector'
# -----------------------------
# Collector Assignments and history
# -----------------------------
from datetime import date
from django.shortcuts import render
from .models import PickupRequest
def collector_assignments(request):
    collector = request.user  
    today = date.today()
    # Step 1: Automatically mark overdue pickups as Missed
    PickupRequest.objects.filter(
        assigned_collector=collector,
        status__in=["Pending", "In-Progress", "In Progress"],
        pickup_date__lt=today
    ).update(status="Missed")
    # Step 2: Fetch only active assignments (Pending / In-Progress), sorted by date and time
    assignments = PickupRequest.objects.filter(
        assigned_collector=collector,
        status__in=["Pending", "In-Progress", "In Progress"]
    ).order_by('pickup_date', 'pickup_time')
    print("Active Assignments for", collector.email)
    for a in assignments:
        print(a.id, a.status, a.pickup_date)
    return render(
        request,
        'ecotracksys/collector_dashboard/my_assignment.html',
        {'assignments': assignments}
    )
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LeaveRequest
from accounts.models import CustomUser
# --- Helper: check admin role ---
def is_admin(user):
    return user.is_authenticated and user.role == "admin"
# --- Admin: view all leave requests ---
@user_passes_test(is_admin)
def leave_request_management(request):
    """
    Admin can view all leave requests from collectors.
    """
    leave_requests = LeaveRequest.objects.select_related("collector").all().order_by("-created_at")
    return render(request, "ecotracksys/admin_dashboard/leave_req_management.html", {"leave_requests": leave_requests})
# --- Admin: approve/reject leave ---
@user_passes_test(is_admin)
def update_leave_status(request, leave_id, status):
    """
    Admin can approve or reject a leave request.
    """
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    if status not in ["Approved", "Rejected"]:
        messages.error(request, "Invalid status.")
    else:
        leave_request.status = status
        leave_request.save()
        messages.success(request, f"Leave request {status.lower()}.")
    return redirect("ecotracksys:leave_req_management")
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import LeaveRequest
# Admin - Leave Request Management Page
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import LeaveRequest
def leave_request_management(request):
    pending = LeaveRequest.objects.filter(status="Pending").order_by('start_date')
    approved = LeaveRequest.objects.filter(status="Approved").order_by('start_date')
    rejected = LeaveRequest.objects.filter(status="Rejected").order_by('start_date')
    return render(request, 'ecotracksys/admin_dashboard/leave_req_management.html', {
        'pending_leaves': pending,
        'approved_leaves': approved,
        'rejected_leaves': rejected,
    })
def leave_request_action(request):
    """
    Handle POST request to approve or reject a leave.
    """
    if request.method == "POST":
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')
        note = request.POST.get('note')  # Optional remarks
        leave = get_object_or_404(LeaveRequest, id=leave_id)
        if action.lower() == 'approve':
            leave.status = 'Approved'
            messages.success(request, f"{leave.collector.email}'s leave approved.")
        elif action.lower() == 'reject':
            leave.status = 'Rejected'
            messages.success(request, f"{leave.collector.email}'s leave rejected.")
        else:
            messages.error(request, "Invalid action.")
        leave.save()
        return redirect('ecotracksys:leave_request_management')
    else:
        return redirect('ecotracksys:leave_request_management')
def leave_request_action_ajax(request):
    """Handles AJAX requests to approve or reject leave requests.Returns JSON with new status."""
    if request.method == "POST" and request.is_ajax():
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')
        note = request.POST.get('note', '')
        leave = get_object_or_404(LeaveRequest, id=leave_id)
        if action.lower() == 'approve':
            leave.status = 'Approved'
        elif action.lower() == 'reject':
            leave.status = 'Rejected'
        else:
            return JsonResponse({'success': False, 'message': 'Invalid action.'})
        leave.save()
        return JsonResponse({
            'success': True,
            'leave_id': leave.id,
            'new_status': leave.status
        })
    return JsonResponse({'success': False, 'message': 'Invalid request.'})
# Admin - Approve / Reject Leave Request
def update_leave_status(request, leave_id, action):
    """
    Admin can approve or reject a collector's leave request.
    """
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    if action == 'approve':
        leave_request.status = 'Approved'
        messages.success(request, f"{leave_request.collector.email}'s leave approved.")
    elif action == 'reject':
        leave_request.status = 'Rejected'
        messages.success(request, f"{leave_request.collector.email}'s leave rejected.")
    else:
        messages.error(request, "Invalid action.")
        return redirect('ecotracksys:leave_request_management')
    leave_request.save()
    return redirect('ecotracksys:leave_request_management')
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
@require_POST
@login_required
def start_assignment(request, pk):
    try:
        job = PickupRequest.objects.get(pk=pk, collector=request.user)
        job.status = "Enroute"
        job.save()
        return JsonResponse({"success": True, "status": "Enroute"})
    except PickupRequest.DoesNotExist:
        return JsonResponse({"success": False, "error": "Not found"}, status=404)
@require_POST
@login_required
def complete_assignment(request, pk):
    try:
        job = PickupRequest.objects.get(pk=pk, collector=request.user)
        job.status = "Completed"
        job.save()
        return JsonResponse({"success": True, "status": "Completed"})
    except PickupRequest.DoesNotExist:
        return JsonResponse({"success": False, "error": "Not found"}, status=404)
#collector
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PickupRequest   # make sure this is your model
@login_required
def raise_issue(request, job_id):
    if request.method == "POST":
        job = get_object_or_404(PickupRequest, id=job_id, collector=request.user)
        description = request.POST.get("description")
        if not description:
            return JsonResponse({"success": False, "error": "Description is required"})
        issue = Issue.objects.create(
            pickup_request=job,   # ✅ correct field name
            collector=request.user,
            description=description,
        )
        return JsonResponse({
            "success": True,
            "issue_id": issue.id,
            "message": "Issue submitted successfully"
        })
    return JsonResponse({"success": False, "error": "Invalid request method"})
@login_required
def cancel_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id, collector=request.user)
    if leave.status == 'Pending':
        leave.status = 'Cancelled'
        leave.save()
        messages.success(request, "Leave request cancelled successfully!")
    else:
        messages.error(request, "Only pending leaves can be cancelled.")
    return redirect('ecotracksys:collector_leave')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ecotracksys.models import LeaveRequest
from django.utils import timezone
from django.http import JsonResponse
from ecotracksys.models import LeaveRequest
def leave_request_action_ajax(request):
    if request.method == "POST" and request.user.is_staff:
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        comment = request.POST.get("note", "")
        try:
            leave = LeaveRequest.objects.get(id=leave_id)
        except LeaveRequest.DoesNotExist:
            return JsonResponse({"success": False, "message": "Leave request not found."})
        # Update status based on action
        if action == "Approve":
            leave.status = "Approved"
        elif action == "Reject":
            leave.status = "Rejected"
        elif action == "Cancel":
            leave.status = "Cancelled"
        else:
            return JsonResponse({"success": False, "message": "Invalid action."})
        leave.admin_comment = comment
        leave.reviewed_at = timezone.now()
        leave.save()
        return JsonResponse({
            "success": True,
            "leave_id": leave.id,
            "new_status": leave.status
        })
    return JsonResponse({"success": False, "message": "Invalid request or permission denied."})
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PickupRequest
@login_required
def update_assignment_status(request, assignment_id):
    """Collector can update assignment status: Completed or Missed."""
    assignment = get_object_or_404(PickupRequest, id=assignment_id, collector=request.user)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "completed" and assignment.status in ["Pending", "In Progress"]:
            assignment.status = "Completed"
            messages.success(request, "Assignment marked as completed 🎉")
        elif action == "missed" and assignment.status in ["Pending", "In Progress"]:
            assignment.status = "Missed"
            messages.warning(request, "Assignment marked as missed ❌")
        else:
            messages.info(request, f"Cannot update status from {assignment.status}")
        assignment.save()
    return redirect("ecotracksys:collector_assignments")
# ecotracksys/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import PickupRequest
@login_required
def update_pickup_status(request, pickup_id, new_status):
    """
    Collector updates their assigned pickup status.
    Allowed: Completed, Missed
    """
    pickup = get_object_or_404(PickupRequest, id=pickup_id)
    # Only the assigned collector can update
    if pickup.collector != request.user:
        return HttpResponseForbidden("You are not assigned to this pickup.")
    allowed_statuses = ["Completed", "Missed"]
    if new_status not in allowed_statuses:
        messages.error(request, "Invalid status update.")
        return redirect("ecotracksys:collector_assignments")
    # Update the status correctly
    pickup.status = new_status
    pickup.save()
    messages.success(request, f"Pickup #{pickup.id} marked as {new_status}.")
    return redirect("ecotracksys:collector_assignments")
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
@require_POST
@login_required
def start_shift(request):
    user = request.user
    if getattr(user, "role", None) != "collector":
        return JsonResponse({"error": "forbidden"}, status=403)
    user.shift_active = True
    user.save(update_fields=["shift_active"])
    return JsonResponse({"ok": True, "shift_active": True})
@require_POST
@login_required
def end_shift(request):
    try:
        shift = CollectorShift.objects.filter(collector=request.user, is_active=True).latest("start_time")
        shift.end_shift()
        return JsonResponse({"success": True, "status": "ended"})
    except CollectorShift.DoesNotExist:
        return JsonResponse({"success": False, "error": "No active shift"}, status=400)
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import PickupRequest
@login_required
def collector_start_assignment(request, pk):
    assignment = get_object_or_404(PickupRequest, pk=pk)
    if assignment.collector != request.user:
        return HttpResponseForbidden("Not allowed")
    assignment.status = "Enroute"  # move to enroute
    assignment.save()
    return redirect('ecotracksys:collector_dashboard')
@login_required
def collector_enroute_assignment(request, pk):
    assignment = get_object_or_404(PickupRequest, pk=pk)
    if assignment.collector != request.user:
        return HttpResponseForbidden("Not allowed")
    # optionally, mark a timestamp for enroute
    assignment.status = "Enroute"
    assignment.save()
    return redirect('ecotracksys:collector_dashboard')
@login_required
def collector_complete_assignment(request, pk):
    assignment = get_object_or_404(PickupRequest, pk=pk)
    if assignment.collector != request.user:
        return HttpResponseForbidden("Not allowed")
    assignment.status = "Done"  # mark completed
    assignment.save()
    return redirect('ecotracksys:collector_dashboard')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification
from django.shortcuts import render
from .models import Notification
def admin_notifications(request):
    status = request.GET.get("status", "all")
    if status == "read":
        notifications = Notification.objects.filter(status="read").order_by("-created_at")
    elif status == "unread":
        notifications = Notification.objects.filter(status="unread").order_by("-created_at")
    else:  # "all"
        notifications = Notification.objects.all().order_by("-created_at")
    return render(request, "ecotracksys/admin_dashboard/admin_notifications.html", {
        "notifications": notifications,
        "status": status,
    })
@login_required
def citizen_notifications(request):
    if request.user.role != "citizen":
        return render(request, "403.html", status=403)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "notifications.html", {"notifications": notifications})
from django.http import JsonResponse
from .models import Notification
# ecotracksys/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
@login_required
def mark_notification_read(request):
    if request.method == "POST":
        notif_id = request.POST.get("notif_id")
        try:
            notif = Notification.objects.get(id=notif_id, user=request.user)
            notif.status = "read"
            notif.save()
            return JsonResponse({"success": True})
        except Notification.DoesNotExist:
            return JsonResponse({"success": False, "error": "Notification not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})
@login_required
def mark_notification_unread(request):
    if request.method == "POST":
        notif_id = request.POST.get("notif_id")
        try:
            notif = Notification.objects.get(id=notif_id, user=request.user)
            notif.status = "unread"
            notif.save()
            return JsonResponse({"success": True})
        except Notification.DoesNotExist:
            return JsonResponse({"success": False, "error": "Notification not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PickupRequest
from django.contrib.auth.decorators import login_required
@login_required
def complete_pickup(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        entered_otp = request.POST.get('otp')
        pickup = PickupRequest.objects.filter(id=job_id, assigned_collector=request.user).first()
        if not pickup:
            return JsonResponse({'success': False, 'error': 'Pickup not found or not assigned to you.'})
        if pickup.otp != entered_otp:
            return JsonResponse({'success': False, 'error': 'Invalid OTP.'})
        # Mark as completed
        pickup.status = 'Completed'
        pickup.otp = ''
        pickup.save()
        return JsonResponse({'success': True, 'message': '✅ Assignment marked as Completed!'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
def delete_collector(request, collector_id):
    collector = get_object_or_404(User, pk=collector_id, role="collector")
    if request.method == "POST":
        collector.delete()
        return redirect("ecotracksys:collector_management")
    return redirect("ecotracksys:collector_management")
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from .models import Notification
def delete_notification(request, pk):
    if request.method == "POST":
        notif = get_object_or_404(Notification, pk=pk)
        notif.delete()
        return JsonResponse({"success": True})
    return HttpResponseNotAllowed(["POST"])
# Bulk delete
def delete_selected_notifications(request):
    if request.method == "POST":
        ids = request.POST.getlist("ids[]")  # from AJAX
        Notification.objects.filter(id__in=ids, user=request.user).delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)
# ecotracksys/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# Import your Notification model. If it's in another app, adjust the import path.
from .models import Notification
@login_required
@require_POST
def toggle_read_notification(request, notif_id):
    """
    Toggle the boolean `read` on the notification and return JSON.
    Expects POST (CSRF token will be checked by middleware).
    """
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.read = not notif.read
    notif.save()
    return JsonResponse({
        "status": "success",
        "msg": "Marked as read" if notif.read else "Marked as unread",
        "read": notif.read
    })
@login_required
@require_POST
def delete_notification(request, notif_id):
    """
    Delete the notification and return JSON.
    Expects POST.
    """
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.delete()
    return JsonResponse({
        "status": "success",
        "msg": "Notification deleted"
    })
from django.core.mail import send_mail
send_mail(
    "Test Console Email",
    "This is a test.",
    "from@example.com",
    ["to@example.com"]
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
@login_required
def collector_change_password(request):
    """
    Allow a logged-in collector to change their password.
    """
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user

        # Check current password
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        # Check if new passwords match
        elif new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
        else:
            # Update password
            user.set_password(new_password)
            user.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been updated successfully.")
            return redirect("ecotracksys:collector_profile")
    return render(request, "ecotracksys/collector_dashboard/change_password.html")
