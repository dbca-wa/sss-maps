import logging
import mimetypes

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from .permissions import IsApiUser
from .utils import get_content_file_from_base64
from .models import MapLinkedFile
from .utils import check_file_exists
logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsApiUser])
def store_map_pdf(request):
    
    uploaded_file = request.POST.get("base64_file")
    hash_value = request.POST.get("hash")
    extension = request.POST.get("extension")
    if not hash_value or not extension:
        return JsonResponse({"success": False, "message": "Hash value and File extension are required"}, status=status.HTTP_400_BAD_REQUEST)
    if uploaded_file:
        filename = f"{hash_value}.{extension}"
        if MapLinkedFile.objects.filter(hash=hash_value).exists() or check_file_exists(filename):
            return JsonResponse({"success": False, "message": "File hash already exists"}, status=status.HTTP_400_BAD_REQUEST)

        content_file = get_content_file_from_base64(uploaded_file, filename=filename)
        if not content_file:
            return JsonResponse({"success": False, "message": "Error processing the file"}, status=status.HTTP_400_BAD_REQUEST)

        new_obj = MapLinkedFile.objects.create(file=content_file, hash=hash_value, extension=extension)
        return JsonResponse({'success': True, 'message': 'Success', 'data': new_obj.file.url}, status=status.HTTP_201_CREATED)    
    else:
        return JsonResponse({"success": False, 'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_file(request, hash, extension):
    map_file = get_object_or_404(MapLinkedFile, hash=hash, extension=extension)
    file = map_file.file
    if file is None:
        return HttpResponse("File doesn't exist", status=status.HTTP_404_NOT_FOUND)

    file_data = None
    with open(file.path, 'rb') as f:
         file_data = f.read()
         f.close()
    return HttpResponse(file_data, content_type=mimetypes.types_map['.'+str(extension)])