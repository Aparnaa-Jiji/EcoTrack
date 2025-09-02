#miniproject/ecotrack/ecotrack/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from ecotracksys import views as ecotracksys_views

urlpatterns = [
    path('admin/', admin.site.urls,),                 # Default Django admin
    path('accounts/', include('accounts.urls')),    # Login, registration, password reset
    path('dashboard/', include('ecotracksys.urls')),  # All custom dashboards
    path('', ecotracksys_views.home, name='index')
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from ecotracksys import views

urlpatterns += [
    path('dashboard/admin/collectors/toggle-status/<int:collector_id>/', 
         views.toggle_collector_status, name='toggle_collector_status'),
]
