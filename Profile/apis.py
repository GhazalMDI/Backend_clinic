# import jdatetime
# import environ
# from django.shortcuts import get_object_or_404
# from django.core.exceptions import ValidationError
# from rest_framework_simplejwt.authentication import JWTAuthentication



# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated


# from Accounts.models import AddressModel, User
# from Accounts.serializers import AddressSerializers, UserSerializers, OtpSerializers
# from utils.StandardResponse import get_Response
# from utils.neshan_api import map
# from utils.sms import send_code
# from utils.imageCompress import compress_image
# from Doctor.models import *
# from Doctor.serializers import DoctorSerializers, WorkingHourSerializers, EducationDetailsSerializers, \
#     CertificateSerializers, AcademicFieldSerializers


# class ProfileApi(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = UserSerializers


#     def get(self, request):
#         if request.user and request.user.is_authenticated:
#             if user := User.objects.filter(phone_number=request.user).first():
#                 if not user.is_doctor:
#                     return get_Response(
#                         success=True,
#                         message='به پروفایل خوش آمدید',
#                         data={
#                             'status_doctor': False,
#                             'user': self.serializer_class(user).data,
#                         },
#                         status=200,
#                     )
                
#                 else:
#                     if doctor := DoctorModel.objects.filter(user=user).first():
#                         work_hours = WorkingHourModel.objects.filter(doctor=doctor)
#                         education = EducationDetailsModel.objects.filter(doctor=doctor)
#                         certificates = CertificateModel.objects.filter(doctor=doctor)
#                         academic_field = AcademicFieldModel.objects.all()
#                         return get_Response(
#                             success=True,
#                             message='دکتر گرامی به پروفایل خود خوش آمدید',
#                             data={
#                                 'status_doctor': True,
#                                 'user': DoctorSerializers(doctor).data,
#                                 'work_hours': WorkingHourSerializers(work_hours, many=True).data,
#                                 'education': EducationDetailsSerializers(education, many=True).data,
#                                 'certificates': CertificateSerializers(certificates, many=True).data,
#                                 'academic_field': AcademicFieldSerializers(academic_field, many=True).data
#                             },
#                             status=200
#                         )
                        
                        
                        
                        
#                         #  return get_Response(
#                         #             success=True,
#                         #             status=200,
#                         #             message='دکتر عزیز به پروفایل خوش آمدید',
#                         #             data=DoctorSerializers(doctor).data,
#                         #         )

                        
#                 #         if educationId := request.query_params.get('edit_edu'):
#                 #             print('hi')
#                 #             print(educationId)
#                 #             if education := EducationDetailsModel.objects.filter(id=educationId, doctor=doctor).first():
#                 #                 print('eduaction get')
#                 #                 education_serializers = EducationDetailsSerializers(instance=education,
#                 #                                                                     data=request.data, partial=True)
#                 #                 if education_serializers.is_valid():
#                 #                     education_serializers.save()
#                 #                     return get_Response(
#                 #                         success=True,
#                 #                         status=200,
#                 #                         message='رکورد تحصیللات با موفقیت ویرایش شد',
#                 #                         data=education_serializers.data,
#                 #                     )

                      
#             return get_Response(
#                 success=False,
#                 message='کاربری یافت نشد ',
#                 status=401
#             )

#                 # return get_Response(
#                 #     success=True,
#                 #     message='خطایی رخ داده است',
#                 #     status=404
#                 # )

#     def put(self, request):
#         max_upload_size = 10 * 1024 * 1024  # 10MB
#         max_size = 150 * 1024  # 150KB

#         if request.user and request.user.is_authenticated:
#             print('authenticated')
#             if user := User.objects.filter(phone_number=request.user).first():
#                 if user.is_doctor == True:
#                     print('is doctor!!')
#                     if doctor := DoctorModel.objects.filter(user=user).first():
#                         print('doctor found')
#                         if image := request.FILES.get('image'):
#                             print('the image is here')
#                             print(image.size)
#                             if image.size > max_upload_size:
#                                 return get_Response(
#                                     success=False,
#                                     status=400,
#                                     message='the image is longer than 10 Mb'
#                                 )
#                             if image.size > max_size:
#                                 image = compress_image(image)
#                             if doctor.image:
#                                 print('last image is delete')
#                                 doctor.image.delete()
#                             doctor.image = image
#                             doctor.save()
#                             return get_Response(
#                                 success=True,
#                                 status=200,
#                                 message='the image profile is success',
#                                 data={'image_url': doctor.image.url}
#                             )
#                         return get_Response(
#                             success=False,
#                             status=400,
#                             message='the serializers is not valid',
#                         )
#                 return get_Response(
#                     success=False,
#                     status=400,
#                     message='the doctor is not found',
#                 )

#             return get_Response(
#                 success=False,
#                 status=400,
#                 message='the user is not valid',
#             )

#         return get_Response(
#             success=False,
#             status=401,
#             message='the authenticated faild',
#         )

#     def patch(self, request):
#         if request.user and request.user.is_authenticated:
#             if user := User.objects.filter(phone_number=request.user).first():
#                 print('the user')
#                 if user.is_doctor == True:
#                     print('the doctor')
#                     print("Request Data:", request.data)
#                     doctor = DoctorModel.objects.filter(user=user).first()
#                     if educationId := request.data.get('edit_edu'):
#                         print('hi')
#                         print(educationId)
#                         if education := EducationDetailsModel.objects.filter(id=educationId, doctor=doctor).first():
#                             print('eduaction get')
#                             education_serializers = EducationDetailsSerializers(instance=education,
#                                                                                 data=request.data, partial=True)
#                             print('hi 3')
#                             if education_serializers.is_valid():
#                                 print('ok')
#                                 education_serializers.save()
#                                 print('serializer is save!')
#                                 return get_Response(
#                                     success=True,
#                                     status=200,
#                                     message='رکورد تحصیللات با موفقیت ویرایش شد',
#                                     data=education_serializers.data,
#                                 )
#                             if not education_serializers.is_valid():
#                                 print("Doctor serializer errors:", education_serializers.errors)
#                     user_data = {
#                         "first_name": request.data.get('first_name'),
#                         "last_name": request.data.get("last_name"),
#                         "birthday": request.data.get("birthday"),
#                         "bio": request.data.get("bio")
#                     }
#                     user_serializer = UserSerializers(data=user_data, instance=user, partial=True)
#                     if user_serializer.is_valid():
#                         user_serializer.save()
#                     srz = DoctorSerializers(data=request.data, instance=doctor, partial=True)
#                     if srz.is_valid():
#                         srz.save()

#                         updated_data = DoctorSerializers(instance=doctor).data
#                         updated_data['user'] = UserSerializers(instance=user).data

#                         return get_Response(
#                             success=True,
#                             message='the doctor profile is updated ',
#                             status=200,
#                             data=updated_data
#                         )
#                     if not srz.is_valid():
#                         return get_Response(
#                             success=False,
#                             message='داده های ارسال شده معتبر نیست',
#                             status=500,
#                             data=srz.errors
#                         )

#                 else:
#                     srz = self.serializer_class(data=request.data, instance=user, partial=True)
#                     if srz.is_valid():
#                         srz.save()
#                         return get_Response(
#                             success=True,
#                             message='the user profile is updated ',
#                             status=200,
#                             data=srz.data
#                         )

#             return get_Response(
#                 success=False,
#                 message='the user is not found',
#                 status=404,
#             )

#         return get_Response(
#             success=False,
#             message='unauthorized',
#             status=500
#         )

#     def post(self, request):
#         if not request.user or not request.user.is_authenticated:
#             return get_Response(success=False, message='لاگین کنید', status=401)

#         user = User.objects.filter(pk=request.user.id).first()
#         if not user:
#             return get_Response(success=False, message='کاربر مورد نظر یافت نشد', status=400)

#         if not user.is_doctor:
#             return get_Response(success=False, message='شما دسترسی لازم را ندارید', status=401)

#         doctor = DoctorModel.objects.filter(user__id=user.id).first()
#         if not doctor:
#             return get_Response(success=False, message='دکتر یافت نشد', status=400)

#         schedules = request.data.get('schedules', [])  # دریافت لیست برنامه‌های کاری
#         educations = request.data.get('Educations', [])  # دریافت لیست تحصیلا
#         print(educations)
#         if schedules:  # بررسی اینکه `schedules` مقدار داشته باشد
#             if not isinstance(schedules, list):
#                 print('no')
#                 return get_Response(success=False, message='فرمت داده‌های برنامه کاری اشتباه است', status=400)

#             srz = WorkingHourSerializers(data=schedules, many=True, context={'doctor': doctor})
#             print('hi')
#             if srz.is_valid():
#                 srz.save()
#                 return get_Response(
#                     success=True,
#                     message='داده‌های شما ثبت شد',
#                     status=200,
#                     data=srz.data
#                 )

#             return get_Response(success=False, message='خطا در سریالایز کردن داده‌های برنامه کاری', status=400,
#                                 data=srz.errors)

#         elif educations:  # اگر `schedules` مقدار نداشت، ولی `educations` مقدار داشته باشد
#             print('hoo')
#             if not isinstance(educations, list):
#                 return get_Response(success=False, message='فرمت داده‌های تحصیلات اشتباه است', status=400)

#             print('hiiiii education')
#             srz = EducationDetailsSerializers(data=educations, many=True, context={'doctor': doctor})
#             if srz.is_valid():
#                 print('hi')
#                 srz.save()
#                 return get_Response(
#                     success=True,
#                     message='رکورد تحصیلات با موفقیت ثبت شد',
#                     status=200,
#                     data=srz.data
#                 )

#             return get_Response(success=False, message='خطا در سریالایز کردن داده‌های تحصیلات', status=400,
#                                 data=srz.errors)

#         return get_Response(success=False, message='هیچ داده‌ای ارسال نشده است', status=400)

# class ProfileEditDeleteApi(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = UserSerializers

#     def delete(self, request, pk):
#         if request.user and request.user.is_authenticated:
#             action = request.query_params.get('action')
#             match action:
#                 case 'certificate':
#                     return self.delete_certificate(request, pk)
#                 case 'education':
#                     return self.delete_education(request, pk)
#                 case 'working_hour':
#                     return self.delete_workHours(request, pk)
#                 case _:
#                     return get_Response(
#                         status=400,
#                         success=False,
#                         message='invalid action'
#                     )

#         return get_Response(
#             success=False,
#             message='خطا در حذف رکورد',
#             status=400
#         )

#     def delete_certificate(self, request, pk):
#         if request.user and request.user.is_authenticated:
#             if user := User.objects.filter(pk=request.user.id).first():
#                 if user.is_doctor:
#                     doctor = DoctorModel.objects.filter(user__id=user.id).first()
#                     if certificate := get_object_or_404(CertificateModel, pk=pk, doctor=doctor):
#                         certificate.delete()
#                         return get_Response(
#                             success=True,
#                             status=200,
#                             message='گواهینامه مورد نظر حذف شد'
#                         )

#         return get_Response(
#             success=False,
#             message='خطا در حذف رکورد',
#             status=400
#         )

#     def delete_education(self, request, pk):
#         if request.user and request.user.is_authenticated:
#             if user := User.objects.filter(pk=request.user.id).first():
#                 if user.is_doctor:
#                     doctor = DoctorModel.objects.filter(user__id=user.id).first()
#                     if educations := EducationDetailsModel.objects.filter(pk=pk, doctor=doctor).first():
#                         educations.delete()
#                         return get_Response(
#                             success=True,
#                             status=200,
#                             message='رکورد تحصیللات با موفقیت حذف شد'
#                         )
#         return get_Response(
#             success=False,
#             message='خطا در حذف رکورد',
#             status=400
#         )

#     def delete_workHours(self, request, pk):
#         if request.user and request.user.is_authenticated:
#             if user := User.objects.filter(pk=request.user.id).first():
#                 if user.is_doctor:
#                     doctor = DoctorModel.objects.filter(user__id=user.id).first()
#                     if works_hours := WorkingHourModel.objects.filter(pk=pk, doctor=doctor).first():
#                         works_hours.delete()
#                         return get_Response(
#                             success=True,
#                             message='رکورد با موفقیت حذف شد',
#                             status=200
#                         )
#         return get_Response(
#             success=False,
#             message='خطا در حذف رکورد',
#             status=400
#         )


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


from .handlers.doctor_handler import DoctorHandler
from .handlers.education_handler import EducationHandler
from .handlers.certificate_handler import CertificateHandler
from .handlers.workinghour_handler import WorkingHourHandler
from .handlers.Profile_handler import ProfileHandler
from utils.StandardResponse import get_Response


from Doctor.serializers import (
    UserSerializers, DoctorSerializers, EducationDetailsSerializers,
    WorkingHourSerializers, CertificateSerializers, AcademicFieldSerializers
)

class ProfileApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializers

    @extend_schema(
        summary="دریافت پروفایل",
        description="بازگرداندن اطلاعات پروفایل کاربر یا دکتر",
        responses={
            200: DoctorSerializers,
            401: OpenApiTypes.STR,
            404: OpenApiTypes.STR
        }
    )
    def get(self, request):
        return ProfileHandler.get_profile(request.user)

    @extend_schema(
        summary="آپلود عکس پروفایل",
        description="آپلود و بروزرسانی عکس پروفایل دکتر",
        request=None,
        responses={200: OpenApiTypes.STR, 400: OpenApiTypes.STR, 401: OpenApiTypes.STR}
    )
    def put(self, request):
        return DoctorHandler.update_image(request.user, request.FILES.get("image"))

    @extend_schema(
        summary="ویرایش پروفایل",
        description="ویرایش اطلاعات کاربر یا دکتر",
        request=EducationDetailsSerializers,
        responses={
            200: DoctorSerializers,
            400: OpenApiTypes.STR,
            404: OpenApiTypes.STR
        }
    )
    def patch(self, request):
        return ProfileHandler.update_profile(request.user, request.data)

    @extend_schema(
        summary="ثبت برنامه کاری یا تحصیلات",
        description="ثبت برنامه‌های کاری یا رکورد تحصیلات برای دکتر",
        request=EducationDetailsSerializers,
        responses={
            201: EducationDetailsSerializers,
            400: OpenApiTypes.STR,
            403: OpenApiTypes.STR
        }
    )
    def post(self, request):
        return ProfileHandler.create_schedule_or_education(request.user, request.data)


class ProfileEditDeleteApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        summary="حذف رکورد تحصیلی، گواهینامه یا ساعت کاری",
        description="با پارامتر query string action نوع حذف مشخص می‌شود",
        parameters=[
            OpenApiParameter(name='action', description='نوع حذف: certificate, education, working_hour',
                             required=True, type=OpenApiTypes.STR)
        ],
        responses={
            200: OpenApiTypes.STR,
            400: OpenApiTypes.STR,
            401: OpenApiTypes.STR,
            404: OpenApiTypes.STR
        }
    )
    def delete(self, request, pk):
        if not request.user or not request.user.is_authenticated:
            return get_Response(success=False, message='خطا در احراز هویت', status=401)

        action = request.query_params.get('action')
        if action == 'certificate':
            return CertificateHandler.delete_certificate(request.user, pk)
        elif action == 'education':
            return EducationHandler.delete_education(request.user, pk)
        elif action == 'working_hour':
            return WorkingHourHandler.delete_workinghour(request.user, pk)

        return get_Response(success=False, message='invalid action', status=400)



class AddressApi(APIView):
        # SERIALIZERS_CLASS =

    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        try:
            if lat and lng:
                location = map(lat=float(lat), lng=float(lng))
                return get_Response(success=True, message='آدرس موقعیت مکانی', data=location, status=200)
        except ValidationError as e:
            return get_Response(
                success=False,
                message=e.message,
                data=None,
                status=400
            )

    def post(self, request):
        try:
            data = request.data
            ldsrz = AddressSerializers(data=data)
            if ldsrz.is_valid():
                vd = ldsrz.validated_data
                user_address = AddressModel.objects.create(
                    formatted_address=vd.get('formatted_address'),
                    state=vd.get('state'),
                    county=vd.get('county'),
                    neighbourhood=vd.get('neighbourhood')
                )
                # user_address = AddressSerializers.create(validated_data=vd)
                return get_Response(
                    success=True,
                    message='آدرس با موفقیت ثبت شد',
                    data=AddressSerializers(user_address).data,
                    status=201
                )

            return get_Response(
                success=False,
                message=ldsrz.errors,
                status=400
            )

        except ValidationError as e:
            return get_Response(success=False, message=e.message, status=400)
