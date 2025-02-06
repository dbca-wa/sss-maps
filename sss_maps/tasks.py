
import requests
import requests.cookies
from requests.auth import HTTPBasicAuth

import logging
import hashlib
import io

from django.conf import settings


logger = logging.getLogger(__name__)
