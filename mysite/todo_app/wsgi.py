"""
WSGI config for todo_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_app.settings')
sys.path.append('D:/DjangoStuff/my_app')
sys.path.append('D:/DjangoStuff/my_app/todo_app')
application = get_wsgi_application()
