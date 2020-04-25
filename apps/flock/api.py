from rest_framework import viewsets, status, routers, mixins, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from django.core.exceptions import ObjectDoesNotExist

from apps.flock import serializers, models


class EventViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.EventSerializer
    permission_classes = (AllowAny,)
    parser_classes = (CamelCaseJSONParser,)

    @action(detail=False, methods=['post'], url_path='event')
    def event(self, request, *args, **kwargs):
        """ Process incoming events
        """
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['name'] == 'app.install':
            serializer.create()
        elif serializer.validated_data['name'] == 'app.uninstall':
            serializer.delete()
        elif serializer.validated_data['name'] == 'client.slashCommand':
            serializer.command(self.request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeaturedViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserFeaturedSerializer
    permission_classes = (AllowAny,)

    lookup_field = 'user_id'
    lookup_url_kwarg = 'user_id'


    @action(detail=True, methods=['post'], url_path='update')
    def update_featured(self, request, user_id, *args, **kwargs):
        """ Add or delete featured images for a user
        """
        try:
            user = self.get_queryset().get(user_id=user_id)
        except ObjectDoesNotExist:
            raise exceptions.NotFound

        serializer = serializers.FeaturedUpdateSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


router = routers.DefaultRouter()
router.register(r'api/flock', EventViewSet, basename='flock')
router.register(r'api/featured', FeaturedViewSet, basename='featured')
