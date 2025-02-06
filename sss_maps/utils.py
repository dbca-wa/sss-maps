import os
from pathlib import Path
import uuid
import base64
import binascii
from datetime import datetime
from django.core.files.base import ContentFile
from django.conf import settings



def get_file_extension(file_name, decoded_file):
    import imghdr

    extension = imghdr.what(file_name, decoded_file)
    extension = "jpg" if extension == "jpeg" else extension
    return extension

def strip_b64_header(content):
    if ';base64,' in content:
        header, base64_data = content.split(';base64,')
        return base64_data
    return content

def get_content_file_from_base64(content, filename=None):
    base64_data = strip_b64_header(content)
    try:
        decoded_file = base64.b64decode(base64_data)
    except (TypeError, binascii.Error):
        raise Exception("Invalid File Exception")
    if not filename:
        uuid_name = str(uuid.uuid4())[:12]
        file_extension = get_file_extension(uuid_name, decoded_file)
        filename = "{}.{}".format(uuid_name, file_extension)
    
    content_file_obj = ContentFile(decoded_file, name=filename)
    return content_file_obj
'''
    Utility function to get the path of the file to be stored.
    Used at validation and at storing time.
'''
def get_file_path(file_name):
    now = datetime.now()
    time = now.strftime("%Y/%m/%d")
    return 'api/download/{0}/{1}'.format(time, file_name)

def check_pdf_file_exists(file_name):
    file_path = get_file_path(file_name)
    full_path = os.path.join(settings.PRIVATE_MEDIA_ROOT, file_path)
    return os.path.exists(full_path)