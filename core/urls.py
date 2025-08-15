from django.urls import path
from . import views  # Import views from core app

urlpatterns = [

    # User Pickup Requests
    path('dashboard/user/pickup_request/', views.pickup_request_view, name='pickup_request'),  # Pickup request form
    path('dashboard/user/my_requests/', views.my_requests_view, name='my_requests'),          # User's submitted requests

    # Contact Page
    path('contact/', views.contact, name='contact'),  # Contact page for queries or feedback

    path('', views.index, name='index'),  # <-- add this line
]
