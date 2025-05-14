"""
WSGI config for wypozyczalnia project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wypozyczalnia.settings')

application = get_wsgi_application() 