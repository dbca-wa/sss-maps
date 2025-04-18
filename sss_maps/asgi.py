"""ASGI config for the SSS Maps project.

It exposes the ASGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""


# Standard
import os

# Third-Party
from django.core import asgi


# Set Django settings environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sss_maps.settings")

# Create ASGI handler
application = asgi.get_asgi_application()
