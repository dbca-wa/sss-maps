from django.contrib import admin
from django.db.models import OuterRef, Subquery
from .models import MapLinkedFile

admin.site.register(MapLinkedFile)
