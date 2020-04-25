from rest_framework import routers, serializers, viewsets, parsers, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.images import models, serializers


class ImageUploadParser(parsers.FileUploadParser):
    media_type = 'image/*'

class ImageViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = models.ImageModel.objects.all()
    serializer_class = serializers.ImageSerializer
    parser_class = (ImageUploadParser,)
    permission_classes = (AllowAny,)

    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    @action(methods=['post'], detail=False, url_name='upload', url_path='upload')
    def upload(self, request, *args, **kwargs):
        file_serializer = self.serializer_class(data=request.data)
        file_serializer.is_valid(raise_exception=True)
        file_serializer.save()
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, id, *args, **kwargs):
        images = self.get_queryset().filter(id=id)
        serializer = serializers.ImageSerializer(images, many=True)
        return Response(serializer.data)


router = routers.DefaultRouter()
router.register(r'api/images', ImageViewSet, basename='images')