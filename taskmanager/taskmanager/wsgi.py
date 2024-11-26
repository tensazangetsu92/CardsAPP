"""
WSGI config for taskmanager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')

application = get_wsgi_application()


# import os
# import sys
#
# # add your project directory to the sys.path
# project_home = u'/home/rhpt'
# if project_home not in sys.path:
#     sys.path.append(project_home)
#
# # set environment variable to tell django where your settings.py is
# os.environ['DJANGO_SETTINGS_MODULE'] = 'myapp.settings'
#
# # serve django via WSGI
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application
