from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.images import models, utils
from apps.flock.models import User


class ThumbnailSerializer(serializers.Serializer):
    thumbnail = Base64ImageField(use_url=False, max_length=None)


class ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=False, required=True)
    thumbnail = Base64ImageField(use_url=False, required=False)

    class Meta:
        model = models.ImageModel
        fields = ('id', 'name', 'image', 'thumbnail', 'times_used')

    def validate_name(self, name):
        return name.strip()

    def save(self, user):
        thumb = utils.convert_to_thumb(self.get_initial()['image'])

        thumb_serializer = ThumbnailSerializer(data={'thumbnail': thumb})
        thumb_serializer.is_valid(raise_exception=True)
        obj = models.ImageModel(
            **self.validated_data,
            uploaded_by=user,
            thumbnail=thumb_serializer.validated_data['thumbnail']
        )
        obj.save()
        return obj


class ImageMetaSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('image_meta',)

    def save(self):
        for key in self.initial_data.get('image_meta', {}).keys():
            print('processing key ',key)
            if key in self.data['image_meta']:
                print('key in data!')
                setattr(self.instance, key, self.initial_data['image_meta'][key])
        return self.instance.save()
