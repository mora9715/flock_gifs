import socket
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH': True,
    'LOGIN_URL': r'/admin',
    'VALIDATOR_URL': None,
    'DEFAULT_API_URL': "https://{}".format(socket.gethostname()),
}

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
    permission_classes=(permissions.AllowAny,),
)