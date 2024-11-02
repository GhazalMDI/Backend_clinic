from rest_framework.views import APIView
from rest_framework.response import Response

from Home.serializers import BannerSerializers
from Home.models import BannerModel, ImageModel
from AboutUs.models import AboutUsModel
from AboutUs.serializers import AboutUsSerializers, ImageSerializers


class HomeAPI(APIView):
    def get(self, request):
        banners = BannerModel.objects.all()
        abouts = AboutUsModel.objects.all()
        bsrz = BannerSerializers(banners, many=True)
        asrz = AboutUsSerializers(abouts, many=True)
        return Response(
            {
                'data': {
                    'banners': bsrz.data,
                    'abouts': asrz.data,
                }
            }
        )
