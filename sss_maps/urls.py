"""
URL configuration for layerCacheService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path

from django import conf
from django import urls
from . import api as sss_maps_api


admin.site.site_header = conf.settings.PROJECT_TITLE
admin.site.index_title = conf.settings.PROJECT_TITLE
admin.site.site_title = conf.settings.PROJECT_TITLE


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/store_map_pdf/', sss_maps_api.store_map_pdf),
    re_path(r'^download/(?P<hash>\w+).(?P<extension>\w\w\w)$', sss_maps_api.get_file, name='get_file'),
    re_path(r'^download/(?P<hash>\w+).(?P<extension>\w\w\w\w)$', sss_maps_api.get_file, name='get_file2'),
]
