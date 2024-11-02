from rest_framework import serializers
from Home.models import BannerModel, ImageModel


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = '__all__'
        read_only_fields = ['id']


class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = BannerModel
        fields = '__all__'
        read_only_fields = ['id']
