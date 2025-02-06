from rest_framework import serializers
from .models import MapLinkedFile

class CreateMapLinkedFileSerializer(serializers.Serializer):
    base64_file = serializers.CharField(required=True, max_length=50000)
    filename = serializers.CharField(required=True, max_length=500)
    
