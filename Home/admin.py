from django.contrib import admin
from Home.models import *


@admin.register(BannerModel)
class BannerModelAdmin(admin.ModelAdmin):
    fields = ('image', 'description')


@admin.register(ImageModel)
class ImageAdmin(admin.ModelAdmin):
    fields = ('type', 'img', 'about')
