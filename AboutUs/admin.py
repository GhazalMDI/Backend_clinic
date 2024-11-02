from django.contrib import admin
from AboutUs.models import AboutUsModel


@admin.register(AboutUsModel)
class AboutUsModelAdmin(admin.ModelAdmin):
    fields = ('title', 'description')
