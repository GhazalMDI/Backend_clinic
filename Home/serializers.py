from rest_framework import serializers
from Home.models import BannerModel, ImageModel,AboutUsModel


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



class AboutUsSerializers(serializers.ModelSerializer):
    images_about = ImageSerializers(many=True, read_only=True)

    class Meta:
        model = AboutUsModel
        fields = ['title', 'description', 'images_about']
        read_only_fields = ('id',)
