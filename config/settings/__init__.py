"""
Cut out important data from git repository
base.py holds all default data
data.py holds all private data (needs to be copied from data_sample.py first
alternatively you can use environmentals
"""
from os import environ
from django.core.management.utils import get_random_secret_key
from .base import *
from .parser import SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_CONFIG


SQLITE_CONFIG = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

# Debug toolbar:
SHOW_TOOLBAR_CALLBACK = 'config.settings.debug_toolbar_enabled'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: DEBUG
}

DATABASES = {
    'default': DB_CONFIG or SQLITE_CONFIG
}
