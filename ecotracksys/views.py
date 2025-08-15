# ecotracksys/views.py

from datetime import timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from .models import PickupRequest, Notification
from .forms import ComplaintForm
from accounts.models import CustomUser


# ===========================
# Cancel Pickup Request API (POST)
# ===========================
@login_required
@require_POST
def cancel_pickup_request(request):
    """
    Allows a user to cancel their pickup request.
    Validates ownership and status before cancelling.
    """
    request_id = request.POST.get('request_id')
    if not request_id:
        return JsonResponse({'error': 'Request ID missing'}, status=400)

    try:
        pickup_request = PickupRequest.objects.get(id=request_id, email=request.user.email)
    except PickupRequest.DoesNotExist:
        return HttpResponseForbidden("You don't have permission to cancel this request.")

    if pickup_request.status in ['Cancelled', 'Completed']:
        return JsonResponse({'error': f'Request is already {pickup_request.status.lower()}.'}, status=400)

    pickup_request.status = 'Cancelled'
    pickup_request.save()

    return JsonResponse({'success': True, 'message': 'Pickup request cancelled.'})


# ===========================
# Raise Complaint View
# ===========================
@login_required
def raise_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('complaint_success')
    else:
        form = ComplaintForm()
    return render(request, 'ecotracksys/user_dashboard/raise_complaint.html', {'form': form})


# ===========================
# Complaint Submission Success View
# ===========================
@login_required
def complaint_success(request):
    """
    Simple page showing complaint was submitted successfully.
    """
    return render(request, 'ecotracksys/complaint_success.html')


# ===========================
# Notifications View
# ===========================
@login_required
def notifications_view(request):
    """
    Displays all notifications for logged-in user.
    Passes counts of unread, today, important notifications to template.
    """
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')

    context = {
        'notifications': notifications,
        'total_count': notifications.count(),
        'unread_count': notifications.filter(status='unread').count(),
        'today_count': notifications.filter(created_at__date=now().date()).count(),
        'important_count': notifications.filter(is_important=True).count(),
    }

    return render(request, 'ecotracksys/user_dashboard/notifications.html', context)


# ===========================
# API: Mark Notification as Read (POST)
# ===========================
@login_required
@require_POST
def mark_notification_read(request):
    notif_id = request.POST.get('notif_id')
    if not notif_id:
        return JsonResponse({'success': False, 'error': 'Notification ID not provided.'})

    try:
        notif = Notification.objects.get(id=notif_id, user=request.user)
        notif.status = 'read'
        notif.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found.'}, status=404)


# ===========================
# API: Mark Notification as Unread (POST)
# ===========================
@login_required
@require_POST
def mark_notification_unread(request):
    notif_id = request.POST.get('notif_id')
    if not notif_id:
        return JsonResponse({'success': False, 'error': 'Notification ID not provided.'})

    try:
        notif = Notification.objects.get(id=notif_id, user=request.user)
        notif.status = 'unread'
        notif.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found.'}, status=404)


# ===========================
# API: Delete Notification (POST)
# ===========================
@login_required
@require_POST
def delete_notification(request):
    notif_id = request.POST.get('notif_id')
    if not notif_id:
        return JsonResponse({'success': False, 'error': 'Notification ID not provided.'})

    try:
        notif = Notification.objects.get(id=notif_id, user=request.user)
        notif.delete()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found.'}, status=404)


# ===========================
# Complaint History View (Citizen)
# ===========================
@login_required
def complaint_history(request):
    """
    Shows the history of complaints raised by the user.
    """
    return render(request, "ecotracksys/user_dashboard/complaint_history.html")

# ecotracksys/views.py

# Import the render function to generate an HttpResponse with a template
from django.shortcuts import render

# Define a view function named 'home' that takes an HttpRequest object 'request'
def home(request):
    # Render and return the 'home.html' template located inside 'ecotracksys' templates folder
    return render(request, 'ecotracksys/landing_page/index.html')

def works(request):
    return render(request, 'ecotracksys/landing_page/works.html')

def about(request):
    return render(request, 'ecotracksys/landing_page/about.html')

from django.shortcuts import render

# ecotracksys/views.py

from django.shortcuts import render
from accounts.models import CustomUser
from .models import PickupRequest, Complaint, Notification
from django.utils.timezone import now

def admin_dashboard(request):
    """
    Admin Dashboard view
    Displays real-time counts for pickups, complaints, collectors, and system alerts.
    """
    
    # Total pickups
    total_pickup_requests = PickupRequest.objects.count()
    completed_pickups = PickupRequest.objects.filter(status="Completed").count()
    active_pickups = PickupRequest.objects.filter(status="In-Progress").count()
    new_pickup_requests = PickupRequest.objects.filter(status="Pending").count()

    # Missed pickups (in our system, could be treated as Cancelled)
    missed_pickups = PickupRequest.objects.filter(status="Cancelled").count()

    # Complaints
    new_complaints = Complaint.objects.filter(status="Pending").count()

    # Leave requests (we don't have the model yet, so set to 0)
    new_leave_requests = 0

    # New collectors — joined in last 7 days
    last_week = now() - timedelta(days=7)
    new_collectors = CustomUser.objects.filter(role="collector", date_joined__gte=last_week).count()

    # System alerts — important unread notifications
    system_alerts = Notification.objects.filter(is_important=True, status="unread").count()

    # Active collectors
    active_collectors = CustomUser.objects.filter(role="collector", is_active=True).count()

    # Collectors on leave today (not available yet — set to 0)
    collectors_on_leave_today = 0

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


# Admin Pickup Management View
def pickup_management(request):
    # Render the pickup management template (adjust path if needed)
    return render(request, 'ecotracksys/admin_dashboard/pickup_management.html')

# Admin Zone Management View
def zone_management(request):
    """
    Renders the Zone Management page for the admin dashboard.
    Admin can view, add, edit, or delete zones here.
    """
    # You can pass dynamic data about zones if needed, e.g.,
    # zones = Zone.objects.all()
    # context = {'zones': zones}

    context = {}  # currently empty, update later with real data

    return render(request, 'ecotracksys/admin_dashboard/zone_route_management.html', context)

def leave_request_management(request):
    """
    Renders the Leave Request Management page for the admin dashboard.
    Admin can view, approve, or reject leave requests here.
    """
    # You can pass dynamic data about leave requests if needed, e.g.,
    # leave_requests = LeaveRequest.objects.all()
    # context = {'leave_requests': leave_requests}

    context = {}  # currently empty, update later with real data

    return render(request, 'ecotracksys/admin_dashboard/leave_req_management.html', context)

def complaint_management(request):
    """
    Renders the Complaint Management page for the admin dashboard.
    Admin can view, respond to, or close complaints here.
    """
    # You can pass dynamic data about complaints if needed, e.g.,
    # complaints = Complaint.objects.all()
    # context = {'complaints': complaints}

    context = {}  # currently empty, update later with real data

    return render(request, 'ecotracksys/admin_dashboard/complaint_management.html', context)

def user_management(request):
    """
    Renders the User Management page for the admin dashboard.
    Admin can view, add, edit, or delete users here.
    """
    # You can pass dynamic data about users if needed, e.g.,
    # users = User.objects.all()
    # context = {'users': users}

    context = {}  # currently empty, update later with real data

    return render(request, 'ecotracksys/admin_dashboard/user_management.html', context)

def collector_management(request):
    """
    Renders the Collector Management page for the admin dashboard.
    Admin can view, add, edit, or delete collectors here.
    """
    # You can pass dynamic data about collectors if needed, e.g.,
    # collectors = Collector.objects.all()
    # context = {'collectors': collectors}

    context = {}  # currently empty, update later with real data

    return render(request, 'ecotracksys/admin_dashboard/collector_management.html', context)

def analytics(request):
    """
    Renders the Analytics page for the admin dashboard.
    Admin can view various analytics and reports here.
    """
    # You can pass dynamic data about analytics if needed, e.g.,
    # reports = Report.objects.all()
    # context = {'reports': reports}

    context = {}  # currently empty, update later with real data

    return render(request, 'ecotracksys/admin_dashboard/analytics.html', context)

def complaint_management(request):
    """
    Renders the Complaint Management page for the admin dashboard.
    Admin can view, respond to, or close complaints here.
    """
    # You can pass dynamic data about complaints if needed, e.g.,
    # complaints = Complaint.objects.all()
    # context = {'complaints': complaints}

    context = {}  # currently empty, update later with real data

    return render(request, 'ecotracksys/admin_dashboard/complaint_management.html', context)

def admin_profile(request):
    """
    Renders the Admin Profile page for the admin dashboard.
    Admin can view and edit their profile information here.
    """
    # You can pass dynamic data about the admin profile if needed, e.g.,
    # admin = request.user
    # context = {'admin': admin}

    context = {}  # currently empty, update later with real data

    return render(request, 'ecotracksys/admin_dashboard/admin_profile.html', context)

def system_setting(request):
    """
    Renders the System Setting page for the admin dashboard.
    Admin can configure system-wide settings here.
    """
    # You can pass dynamic data about system settings if needed, e.g.,
    # settings = SystemSettings.objects.all()
    # context = {'settings': settings}

    context = {}  # currently empty, update later with real data

    return render(request, 'ecotracksys/admin_dashboard/system_setting.html', context)

def collector_dashboard(request):
    """
    Renders the Collector Dashboard page.
    Collectors can view their tasks, history, and profile here.
    """
    # You can pass dynamic data about the collector's dashboard if needed, e.g.,
    # tasks = Task.objects.filter(collector=request.user)
    # context = {'tasks': tasks}

    context = {}  # currently empty, update later with real data

    return render(request, 'collector_dashboard.html', context)

def today_tasks(request):
    """
    Renders the Today Tasks page for the collector dashboard.
    Collectors can view their tasks for today here.
    """
    # You can pass dynamic data about today's tasks if needed, e.g.,
    # tasks = Task.objects.filter(collector=request.user, date_due=datetime.date.today())
    # context = {'tasks': tasks}

    context = {}  # currently empty, update later with real data

    return render(request, 'collector_today_tasks.html', context)

def pickup_history(request):
    """
    Renders the Pickup History page for the collector dashboard.
    Collectors can view their pickup history here.
    """
    # You can pass dynamic data about the pickup history if needed, e.g.,
    # pickups = Pickup.objects.filter(collector=request.user)
    # context = {'pickups': pickups}

    context = {}  # currently empty, update later with real data

    return render(request, 'collector_pickup_history.html', context)

def collector_leave_request(request):
    """
    Renders the Leave Request page for the collector dashboard.
    Collectors can submit leave requests here.
    """
    # You can pass dynamic data about leave requests if needed, e.g.,
    # leave_requests = LeaveRequest.objects.filter(collector=request.user)
    # context = {'leave_requests': leave_requests}

    context = {}  # currently empty, update later with real data

    return render(request, 'collector_leave_request.html', context)

def collector_profile(request):
    """
    Renders the Profile page for the collector dashboard.
    Collectors can view and edit their profile information here.
    """
    # You can pass dynamic data about the collector's profile if needed, e.g.,
    # collector = request.user
    # context = {'collector': collector}

    context = {}  # currently empty, update later with real data

    return render(request, 'collector_profile.html', context)

def collector_settings(request):
    """
    Renders the Settings page for the collector dashboard.
    Collectors can update their account settings here.
    """
    # You can pass dynamic data about the collector's settings if needed, e.g.,
    # settings = CollectorSettings.objects.get(collector=request.user)
    # context = {'settings': settings}

    context = {}  # currently empty, update later with real data

    return render(request, 'collector_settings.html', context)

def citizen_dashboard(request):
    """
    Renders the Citizen Dashboard page.
    Citizens can view their profile, tasks, and history here.
    """
    # You can pass dynamic data about the citizen's dashboard if needed, e.g.,
    # tasks = Task.objects.filter(collector=request.user)
    # context = {'tasks': tasks}

    context = {}  # currently empty, update later with real data

    return render(request, 'citizen_dashboard.html', context)

def citizen_pickup_request(request):
    """
    Renders the Pickup Request page for the citizen dashboard.
    Citizens can submit pickup requests here.
    """
    # You can pass dynamic data about pickup requests if needed, e.g.,
    # pickup_requests = PickupRequest.objects.filter(citizen=request.user)
    # context = {'pickup_requests': pickup_requests}

    context = {}  # currently empty, update later with real data

    return render(request, 'citizen_pickup_request.html', context)

def citizen_history(request):
    """
    Renders the History page for the citizen dashboard.
    Citizens can view their pickup history here.
    """
    # You can pass dynamic data about the citizen's history if needed, e.g.,
    # history = PickupHistory.objects.filter(citizen=request.user)
    # context = {'history': history}

    context = {}  # currently empty, update later with real data

    return render(request, 'citizen_history.html', context)

