from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions
from rest_framework_jwt.compat import gettext_lazy as _

from apps.flock.models import User


class FlockJwtAuthentication(JSONWebTokenAuthentication):
    """
    Custom authentication class that complies with Flock Event Tokens
    """
    def jwt_get_username_from_payload(self, payload):
        """
        Returns userId from payload.
        """
        return payload.get('userId')

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id.
        """
        username = self.jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(user_id=username)
        except User.DoesNotExist:
            msg = _('Invalid token.')
            raise exceptions.AuthenticationFailed(msg)

        return user
