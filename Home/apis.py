from rest_framework.views import APIView
from rest_framework.response import Response

from Home.serializers import BannerSerializers
from Home.models import BannerModel, ImageModel
from AboutUs.models import AboutUsModel
from AboutUs.serializers import AboutUsSerializers, ImageSerializers
from Department.serializers import DepartmentSerializers
from Department.models import DepartmentModel


class HomeAPI(APIView):
    def get(self, request):
        banners = BannerModel.objects.all()
        abouts = AboutUsModel.objects.all()
        department = DepartmentModel.objects.all()
        bsrz = BannerSerializers(banners, many=True)
        asrz = AboutUsSerializers(abouts, many=True)
        dsrz = DepartmentSerializers(department, many=True)
        return Response(
            {
                'data': {
                    'banners': bsrz.data,
                    'abouts': asrz.data,
                    'department': dsrz.data
                }
            }
        )
