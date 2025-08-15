from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ecotracksys.models import PickupRequest, Complaint, CustomUser

# ===========================
# Pickup Request Form View (Citizen)
# ===========================
@login_required
def pickup_request_view(request):
    """
    Render the pickup request form page.
    Citizen uses this page to submit a new waste pickup request.
    Form POST handling can be added later.
    """
    return render(request, 'ecotracksys/user_dashboard/pickup_request.html')


# ===========================
# User's Pickup Requests History View (Citizen)
# ===========================
@login_required
def my_requests_view(request):
    """
    Display the logged-in citizen's pickup requests.
    Filters requests belonging only to the current user.
    Allows users to view the status and details of their past requests.
    """
    user = request.user
    requests_qs = PickupRequest.objects.filter(user=user).order_by('-created_at')

    context = {
        'requests': requests_qs,  # Pass user's requests to the template
    }

    return render(request, 'ecotracksys/user_dashboard/my_requests.html', context)


# ===========================
# Contact Page View
# ===========================
def contact(request):
    """
    Renders the landing page contact form.
    Accessible by any visitor or logged-in user.
    """
    return render(request, 'ecotracksys/landing_page/contact.html')


def index(request):
    return render(request, 'ecotracksys/landing_page/index.html')  # your homepage template

