from rest_framework.views import APIView
from rest_framework.response import Response

from Home.serializers import BannerSerializers , AboutUsSerializers ,ImageSerializers
from Home.models import BannerModel, ImageModel ,AboutUsModel
from Doctor.serializers import DepartmentSerializers
from Doctor.models import DoctorDepartmentModel


class HomeAPI(APIView):
    def get(self, request):
        banners = BannerModel.objects.all()
        abouts = AboutUsModel.objects.all()
        department = DoctorDepartmentModel.objects.all()
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
