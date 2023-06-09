# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

import os

from .base import BASE_DIR


DB_DIR = os.path.dirname(BASE_DIR)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DB_DIR, 'db.sqlite3'),
    }
}
