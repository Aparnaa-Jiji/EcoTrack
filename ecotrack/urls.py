"""
URL configuration for ecotrack project.

The `urlpatterns` list routes URLs to views. 
See https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),                 # Default Django admin
    path('accounts/', include('accounts.urls')),    # Login, registration, password reset
    path('ecotracksys/', include('ecotracksys.urls')),  # Main system app: dashboards, pickups
    path('core/', include('core.urls')),            # Core pages: home, contact, pickup forms
    path('', include('ecotracksys.urls')),  
    path('', core_views.index, name='index'),
    path('dashboard/', include('ecotracksys.urls')),  # all custom dashboards
]
        # Root URL serves the main landing/home page


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
