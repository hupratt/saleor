"""
WSGI config for La_petite_portugaise project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys



from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.dirname(os.path.abspath(__file__))+ '/..'+ '/..')
sys.path.append('/home/ubuntu/Dev/saleor/lib/python3.6')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleor.settings")

application = get_wsgi_application()

try:
    application = get_wsgi_application()
    print('WSGI loaded successfully')
except Exception as err:
    print(err)
