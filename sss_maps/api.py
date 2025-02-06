import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from .permissions import IsUserAuthenticated
from .utils import get_content_file_from_base64
from .models import MapLinkedFile
from .utils import check_pdf_file_exists
logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsUserAuthenticated])
def store_map_pdf(request):
    
    uploaded_file = request.POST.get("base64_file")
    filename = request.POST.get("filename")
    
    if uploaded_file and filename:
        if check_pdf_file_exists(filename):
            return JsonResponse({"success": False, "message": "File name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        content_file = get_content_file_from_base64(uploaded_file, filename=filename)
        if not content_file:
            return JsonResponse({"success": False, "message": "Error processing the file"}, status=status.HTTP_400_BAD_REQUEST)

        new_obj = MapLinkedFile.objects.create(file=content_file)
        return JsonResponse({'success': True, 'message': 'Success', 'data': new_obj.file.url}, status=status.HTTP_201_CREATED)    
    else:
        return JsonResponse({"success": False, 'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
