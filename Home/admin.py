from django.contrib import admin
from Home.models import *


@admin.register(BannerModel)
class BannerModelAdmin(admin.ModelAdmin):
    fields = ('image', 'description')


@admin.register(ImageModel)
class ImageAdmin(admin.ModelAdmin):
    fields = ('type', 'img', 'about')

@admin.register(AboutUsModel)
class AboutUsModelAdmin(admin.ModelAdmin):
    fields = ('title', 'description')
