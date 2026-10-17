from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-devtrack-local-key-string'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'issues',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'devtrack.urls'
DATABASES = {}  # Empty since data uses your native custom OOP model entities
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
