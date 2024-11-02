from rest_framework import serializers
from AboutUs.models import AboutUsModel
from Home.serializers import ImageSerializers


class AboutUsSerializers(serializers.ModelSerializer):
    images_about = ImageSerializers(many=True, read_only=True)

    class Meta:
        model = AboutUsModel
        fields = ['title', 'description', 'images_about']
        read_only_fields = ('id',)
