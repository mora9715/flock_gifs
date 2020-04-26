"""flock_gifs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import socket
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, static

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.images import api as images_api
from apps.flock import api as flock_api

SWAGGER_MAIN_PAGE = {
    "title": "Flock Images API",
    "default_version": "v1",
    "description": "Swagger for Flock Images App API",
    'contact_email': "mora9715@gmail.com",
}


main_data = SWAGGER_MAIN_PAGE.copy()
email = main_data.pop('contact_email')

SWAGGER_SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        **main_data,
        contact=openapi.Contact(
            email=email
        ),
    ),
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^api/swagger/$', SWAGGER_SCHEMA_VIEW.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^', include(images_api.router.urls)),
    url(r'^', include(flock_api.router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
] + static.static('img', document_root='img')
