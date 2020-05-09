from django.db import models
from django.utils.html import mark_safe
from django.conf import settings
# Create your models here.

class ImageModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='img/', blank=False)
    thumbnail = models.ImageField(upload_to='img/', blank=False)
    ts = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey("flock.User", blank=True, null=True, on_delete=models.DO_NOTHING)

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.thumbnail.delete()
        super(ImageModel, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe(f'<img src="http://127.0.0.1:8000/{self.image.name}" height="150" />')

    def thumbnail_tag(self):
        return mark_safe(f'<img src="http://127.0.0.1:8000/{self.thumbnail.name}" height="50" />')

    def max_width(self):
        return settings.FLOCK_ATTACHMENT_WIDTH

    def max_height(self):
        return settings.FLOCK_ATTACHMENT_HEIGHT