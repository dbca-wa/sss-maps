"""WSGI config for the SSS Maps project.

It exposes the WSGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""


# Standard
import os

# Third-Party
from django.core import wsgi


# Set Django settings environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sss_maps.settings")

# Create WSGI handler
application = wsgi.get_wsgi_application()
