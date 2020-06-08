from django.contrib import admin
from apps.images import models
# Register your models here.

@admin.register(models.ImageModel)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)
    list_display = ('id', 'name', 'thumbnail_tag', 'times_used')