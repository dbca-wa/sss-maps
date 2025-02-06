"""SSS MAPS Django Application Permissions."""

# Third-Party
import django
from django.conf import settings
from rest_framework import permissions, request, viewsets
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Typing
from typing import Union
from typing import Any

class IsUserAuthenticated(permissions.BasePermission):
    """Permissions for the a user in the Administrators group."""

    def has_permission(  # type: ignore
        self,
        request: request.Request,
        view: viewsets.GenericViewSet,
    ) -> bool:
        return settings.BYPASS_AUTHENTICATION or request.user.is_authenticated
