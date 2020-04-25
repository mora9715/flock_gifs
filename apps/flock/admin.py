from django.contrib import admin

from apps.flock import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass
