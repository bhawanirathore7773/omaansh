# WSGI config for PythonAnywhere
# Place this in /var/www/yourusername_pythonanywhere_com_wsgi.py

import os
import sys
from pathlib import Path

# Add your project to the path
project_home = '/home/yourusername/hoovale_project'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'hoovale.settings'

# Configure Django
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

if not settings.configured:
    django.setup()

# Get the WSGI application
application = get_wsgi_application()
