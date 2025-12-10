import logging
import mimetypes

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from .permissions import IsApiUser
from .utils import get_content_file_from_base64
from .models import MapLinkedFile
from .utils import check_file_exists
from django.core.cache import cache

logger = logging.getLogger(__name__)

from rest_framework.authentication import SessionAuthentication


class SessionCsrfExemptAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


@api_view(['POST'])
@authentication_classes([SessionCsrfExemptAuthentication])
@permission_classes([IsApiUser])
def store_map_pdf(request):
    hash_value = request.POST.get("hash")
    extension = request.POST.get("extension")
    part_number = int(request.POST.get("part_number"))
    total_parts = int(request.POST.get("total_parts"))
    uploaded_file_chunk = request.POST.get("base64_file")

    if not hash_value or not extension or part_number is None or total_parts is None:
        return JsonResponse({"success": False, "message": "Hash value, File extension, part number, and total parts are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Store received chunks in a cache
    chunk_key = f"{hash_value}_part_{part_number}"
    cache.set(chunk_key, uploaded_file_chunk, timeout=3600)

    # Check if all parts have been received
    all_parts_received = all(cache.get(f"{hash_value}_part_{i}") for i in range(1, total_parts + 1))
    
    if all_parts_received:
        full_file = "".join(cache.get(f"{hash_value}_part_{i}") for i in range(1, total_parts + 1))
        
        # Delete cached chunks manually
        for i in range(1, total_parts + 1):
            cache.delete(f"{hash_value}_part_{i}")

        filename = f"{hash_value}.{extension}"
        if MapLinkedFile.objects.filter(hash=hash_value).exists() or check_file_exists(filename):
            return JsonResponse({"success": False, "message": "File hash already exists"}, status=status.HTTP_400_BAD_REQUEST)

        content_file = get_content_file_from_base64(full_file, filename=filename)
        if not content_file:
            return JsonResponse({"success": False, "message": "Error processing the file"}, status=status.HTTP_400_BAD_REQUEST)

        new_obj = MapLinkedFile.objects.create(file=content_file, hash=hash_value, extension=extension)
        return JsonResponse({'success': True, 'message': 'Success', 'data': new_obj.file.url}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({"success": True, "message": "Chunk received, awaiting more chunks"}, status=status.HTTP_200_OK)


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

@api_view(['GET'])
def status(request):
    total_map_files = MapLinkedFile.objects.count()
    resp = {"status" : 500, "message": "Error with map linked"}
    if total_map_files > 0:
        status = {"status": 200, "message" : "Success loading map count"}

    return HttpResponse(status, content_type=mimetypes.types_map['.json'], status_code=status['status'])
