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

    def __str__(self):
        return self.name

    @property
    def is_authenticated(self):
        return True