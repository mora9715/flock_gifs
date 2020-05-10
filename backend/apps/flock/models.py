from django.db import models

from apps.images.models import ImageModel

# Create your models here.
class User(models.Model):
    user_id = models.CharField(
        max_length=255,
        unique=True
    )
    name = models.CharField(
        max_length=255
    )
    token = models.CharField(
        max_length=255
    )
    featured = models.ManyToManyField(
        ImageModel,
        blank=True,
    )
    max_image_width = models.IntegerField(default=150)
    max_image_height = models.IntegerField(default=150)
    items_per_page = models.IntegerField(default=20)

    def __str__(self):
        return self.name

    @property
    def is_authenticated(self):
        return True

    @property
    def image_meta(self):
        return {
            'max_image_width': self.max_image_width,
            'max_image_height': self.max_image_height,
            'items_per_page': self.items_per_page
        }