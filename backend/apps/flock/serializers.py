import re

from rest_framework import serializers, exceptions
from drf_extra_fields.fields import Base64ImageField

from apps.images.models import ImageModel
from apps.flock.models import User
from apps.flock.clients import FlockAPIClient
from django.conf import settings


class EventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    user_id = serializers.CharField(max_length=100)
    token = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
    )
    chat = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True
    )
    command = serializers.CharField(
        max_length=255,
        required=False,
        allow_null=True
    )
    text = serializers.CharField(
        max_length=255,
        required=False,
        allow_null=True
    )

    def create(self):
        """ Add a new user to app
        """
        # TODO: add logging
        api = FlockAPIClient()
        try:
            response = api.client.roster.listContacts.post()
        except Exception:
            raise exceptions.ParseError

        user = [u for u in response.to_dict if u['id'] == self.validated_data['user_id']]
        if len(user) != 1:
            raise exceptions.ParseError
        name = user[0].get('firstName', '') + ' ' + user[0].get('lastName', '')
        name = re.sub('[^a-zA-Z ]+', '', name).strip()
        obj, created = User.objects.get_or_create(
            user_id=user[0]['id'],
            name=name,
            token=self.validated_data['token']
        )

    def delete(self):
        """ Delete user from app
        """
        try:
            User.objects.get(user_id=self.validated_data['user_id']).delete()
        except User.DoesNotExist:
            # TODO: logging
            pass

    def command(self, request):
        """ Process slash command
        """
        try:
            user = User.objects.get(user_id=self.validated_data['user_id'])
        except User.DoesNotExist:
            # TODO: handle such cases somehow
            raise exceptions.NotFound

        img_name = self.validated_data.get('text', '').strip()

        try:
            img_tag = f"https://{request.META['HTTP_HOST']}/{ImageModel.objects.get(name=img_name).image}"
        except ImageModel.DoesNotExist:
            return True

        request_body = {
            'to': self.validated_data['chat'],
            'attachments': [
                {
                    'color': settings.FLOCK_ATTACHMENT_COLOR,
                    'views': {
                        'image': {
                            'original': {
                                'src': img_tag,
                                'width': settings.FLOCK_ATTACHMENT_WIDTH,
                                'height': settings.FLOCK_ATTACHMENT_HEIGHT
                            }
                        }
                    }
                }
            ]
        }
        api = FlockAPIClient(token=user.token)
        api.client.chat.sendMessage.post(request_body=request_body)



class FeaturedSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=False, required=True)
    thumbnail = Base64ImageField(use_url=False, required=False)
    max_width = serializers.IntegerField()
    max_height = serializers.IntegerField()
    class Meta:
        model = ImageModel
        exclude = ('ts',)


class UserFeaturedSerializer(serializers.ModelSerializer):
    featured = FeaturedSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('featured', 'image_meta')

class FeaturedUpdateSerializer(serializers.Serializer):
    remove = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_null=True
    )
    add = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_null=True
    )

    def update(self, user):
        # Deleting:
        for featured in self.validated_data.get('remove', []):
            try:
                user.featured.remove(ImageModel.objects.get(id=featured))
            except user.DoesNotExist:
                pass

        # Adding:
        for featured in self.validated_data.get('add', []):
            try:
                user.featured.add(ImageModel.objects.get(id=featured))
            except user.DoesNotExist:
                pass