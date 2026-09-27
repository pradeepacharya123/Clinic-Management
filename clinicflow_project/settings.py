import os
from pathlib import Path
import environ
from datetime import timedelta

# -------------------------------------------------------
# Base Directory
# -------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------
# Reading .env file
# -------------------------------------------------------
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# -------------------------------------------------------
# Secret Key & Debug — loaded from .env (never hardcode!)
# -------------------------------------------------------
SECRET_KEY = env('SECRET_KEY')  
DEBUG = env.bool('DEBUG', default=True) #true development mode , false production mode
ALLOWED_HOSTS = ['*']  #allow all domains to access your app , not safe for production
CSRF_TRUSTED_ORIGINS = [
    'https://clinic-management-production-4849.up.railway.app',
]
# -------------------------------------------------------
# Installed Apps
# -------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',         # Django REST Framework
    'crispy_forms',           # Better looking forms
    'crispy_bootstrap5',      # Bootstrap 5 styling for forms
    'django_celery_beat',
    'django_celery_results',

    # Our ClinicFlow apps
    'accounts',
    'patients',
    'doctors',
    'appointments',
    'prescriptions',
    'billing',
    'reports',
    'api',
]

# -------------------------------------------------------
# Middleware
# -------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------------------------------
# URL Configuration
# -------------------------------------------------------
ROOT_URLCONF = 'clinicflow_project.urls'

# -------------------------------------------------------
# Templates — Jinja/Django templating
# -------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # global templates folder
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

# -------------------------------------------------------
# WSGI
# -------------------------------------------------------
WSGI_APPLICATION = 'clinicflow_project.wsgi.application'

# -------------------------------------------------------
# Database — MySQL (all values from .env file)
# -------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# -------------------------------------------------------
# Password Validators
# -------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------
# Internationalization
# -------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'   # Indian timezone ✅
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------
# Static files (CSS, JS)
# -------------------------------------------------------
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# -------------------------------------------------------
# Media files (uploaded images, prescription files)
# -------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------------------------------
# Default primary key
# -------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------
# Crispy Forms — Bootstrap 5 styling
# -------------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# -------------------------------------------------------
# Django REST Framework settings
# -------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # JWT authentication for API
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # Session auth for browsable API
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME' : timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES'     : ('Bearer',),
}

# 💡 What is JWT? When a user logs in via API, instead of creating a session (like websites do), the server gives 
# them a token — a long encrypted string. Every API request must include this token in the header. The server 
# checks the token and knows who you are. This is how mobile apps and React frontends authenticate!

# -------------------------------------------------------
# Login / Logout redirect
# -------------------------------------------------------
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Custom user model
AUTH_USER_MODEL = 'accounts.User'
#💡 Why? By default Django uses its own User model. 
#This line tells Django — "use MY custom User model from the accounts app instead. 

# ======================
# CELERY CONFIGURATION
# ======================
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

# Celery Beat Schedule (Periodic Tasks)
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {

    # Task 1: Check every 15 minutes and send reminders
    'send-appointment-reminders': {
        'task': 'appointments.tasks.send_appointment_reminder',
        'schedule': crontab(minute='*/15'),
    },

    # Task 2: Send daily summary to admin at 8:00 AM every day
    'send-daily-summary': {
        'task': 'appointments.tasks.send_daily_summary',
        'schedule': crontab(hour=8, minute=0),
    },

    # Task 3: Mark past appointments as completed every hour
    'mark-completed-appointments': {
        'task': 'appointments.tasks.mark_completed_appointments',
        'schedule': crontab(minute=0),
    },
}

# ======================
# EMAIL CONFIGURATION
# ======================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER', default='')
ADMIN_EMAIL = env('EMAIL_HOST_USER', default='')