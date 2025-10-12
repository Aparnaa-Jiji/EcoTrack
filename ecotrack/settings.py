# miniproject/ecotrack/ecotrack/settings.py

from pathlib import Path
import os

# ================================
# Paths
# ================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ================================
# Security
# ================================
SECRET_KEY = 'django-insecure-your-secret-key'  # Replace with your actual key
DEBUG = True
ALLOWED_HOSTS = []

# ================================
# Installed Applications
# ================================
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',

    # Project apps
    'accounts',       # Custom user, authentication
    'core',           # Public pages (home, about, contact, pickup form)
    'ecotracksys',    # Dashboards & system logic
]

# ================================
# Middleware
# ================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "accounts.middleware.NoCacheMiddleware",
    
]

# ================================
# URLS & WSGI
# ================================
ROOT_URLCONF = 'ecotrack.urls'

WSGI_APPLICATION = 'ecotrack.wsgi.application'

# ================================
# Templates
# ================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # global templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ================================
# Database (MySQL)
# ================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecotrack_db',      # Change this to your DB name
        'USER': 'ecotrack_user',
        'PASSWORD': 'EcoTrack@123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# ================================
# Authentication
# ================================
AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = 'ecotracksys:dashboard_home'
LOGOUT_REDIRECT_URL = 'index'

# ================================
# Password Validation
# ================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ================================
# Internationalization
# ================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # adjust if needed
USE_I18N = True
USE_TZ = True

# ================================
# Static & Media Files
# ================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "ecotracksys", "static")]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ================================
# Default Primary Key Field Type
# ================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# middleware.py
from django.utils.deprecation import MiddlewareMixin

class DisableBackMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ecotracksys.mca@gmail.com'      # <-- your email
EMAIL_HOST_PASSWORD = 'pglo ybip dyzm impg'   # <-- app password if using Gmail
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
