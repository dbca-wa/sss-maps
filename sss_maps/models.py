from django.db.models import Q
from django.conf import settings
from django.db import models
from django.core.files.storage import FileSystemStorage

from .utils import get_file_path
upload_storage = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)

def upload_to_path(instance, filename):
    return get_file_path(filename)

class MapLinkedFile(models.Model):
    file = models.FileField(max_length=512, upload_to=upload_to_path, storage=upload_storage)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        filename = ''
        return f'{self.hash} - {filename}'


