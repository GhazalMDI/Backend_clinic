import jdatetime
import environ
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from random import randint

from Accounts.models import AddressModel, User, OtpModel
from Accounts.serializers import AddressSerializers, UserSerializers, OtpSerializers
from utils.StandardResponse import get_Response
from utils.neshan_api import map
from utils.sms import send_code
from utils.imageCompress import compress_image
from Doctor.models import *
from Doctor.serializers import DoctorSerializers, WorkingHourSerializers, EducationDetailsSerializers, \
    CertificateSerializers, AcademicFieldSerializers


def create_jwt_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class RegisterApi(APIView):

    def post(self, request):
        data = request.data
        srz = OtpSerializers(data=data)
        if srz.is_valid():
            now = jdatetime.datetime.now()
            phone_number = srz.validated_data.get('phone_number')
            temp_token = AccessToken()
            temp_token['phone_number'] = phone_number
            temp_token.set_exp(lifetime=jdatetime.timedelta(minutes=2))
            if otps := OtpModel.objects.filter(phone_number=phone_number).first():
                exp_time = otps.created + jdatetime.timedelta(minutes=2)
                if now > exp_time:
                    otps.delete()
                else:
                    return Response({
                        'success': True,
                        'message': 'زمان کد قبلی هنوز تمام نشده است',
                        'temp_token': str(temp_token),

                    }, status=200)
            Random_code = randint(100000, 999999)
            OtpModel.objects.create(phone_number=phone_number, random_code=Random_code)
            # print(temp_token)
            # send_code(phone_number, Random_code)

            return Response({
                'success': True,
                'message': 'کد برای شما ارسال شد',
                'temp_token': str(temp_token),
            }, status=200)

        return get_Response(
            success=False,
            message=srz.errors,
            status=400
        )


class VerifyRegisterApi(APIView):

    def post(self, request):
        token = request.headers.get('Authorization')
        print(token)
        user_code = request.data.get('code').strip()
        print(token)
        if not user_code:
            return get_Response(
                success=False,
                message='کد ارسال نشده است',
                status=status.HTTP_404_NOT_FOUND
            )
        if not token:
            return Response({"error": "Token is missing"}, status=status.HTTP_400_BAD_REQUEST)

        token = token.split(' ')[1] if ' ' in token else token
        now = jdatetime.datetime.now()
        try:
            access_token = AccessToken(token)
            print(access_token)
            phone_number = access_token.get('phone_number')
            print(phone_number)
            if otp := OtpModel.objects.filter(phone_number=phone_number).first():
                print(otp.random_code)
                print(user_code)
                otp_expire = otp.created + jdatetime.timedelta(minutes=2)
                if now > otp_expire:
                    return get_Response(
                        success=False,
                        message='کد منقضی شده است',
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if otp.random_code != user_code:
                    return get_Response(
                        success=False,
                        message='رمز وارد شده اشتباه است',
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    otp.delete()
                    if user := User.objects.filter(phone_number=phone_number).first():
                        print(user)
                        tokens = create_jwt_user(user)
                        return get_Response(
                            success=True,
                            message='کاربر عزیز خوش آمدید',
                            status=status.HTTP_200_OK,
                            tokens=tokens
                        )
                    user = User.objects.create(phone_number=phone_number)
                    print(user)
                    tokens = create_jwt_user(user)
                    return get_Response(
                        success=True,
                        message='ثبت نام شام با موفقیت انجام شد.',
                        status=status.HTTP_200_OK,
                        tokens=tokens
                    )
            return get_Response(
                success=False,
                message='کد مورد نطر یافت نشد',
                status=status.HTTP_400_BAD_REQUEST
            )
        except TokenError:
            return Response({"error": "Token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)

    # def create_jwt_user(self, user):
    #     refresh = RefreshToken.for_user(user)
    #     print(refresh)
    #     print(str(refresh.access_token))
    #     return {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token)
    #     }


class ProfileApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializers

    def get(self, request):
        if request.user and request.user.is_authenticated:
            if user := User.objects.filter(phone_number=request.user).first():
                if not user.is_doctor:
                    return get_Response(
                        success=True,
                        message='به پروفایل خوش آمدید',
                        data={
                            'status_doctor': False,
                            'user': self.serializer_class(user).data,
                        },
                        status=200,
                    )
                else:
                    if doctor := DoctorModel.objects.filter(user=user).first():
                        if educationId := request.query_params.get('edit_edu'):
                            print('hi')
                            print(educationId)
                            if education := EducationDetailsModel.objects.filter(id=educationId, doctor=doctor).first():
                                print('eduaction get')
                                education_serializers = EducationDetailsSerializers(instance=education,
                                                                                    data=request.data, partial=True)
                                if education_serializers.is_valid():
                                    education_serializers.save()
                                    return get_Response(
                                        success=True,
                                        status=200,
                                        message='رکورد تحصیللات با موفقیت ویرایش شد',
                                        data=education_serializers.data,
                                    )

                        work_hours = WorkingHourModel.objects.filter(doctor=doctor)
                        education = EducationDetailsModel.objects.filter(doctor=doctor)
                        certificates = CertificateModel.objects.filter(doctor=doctor)
                        academic_field = AcademicFieldModel.objects.all()
                        return get_Response(
                            success=True,
                            message='دکتر گرامی به پروفایل خود خوش آمدید',
                            data={
                                'status_doctor': True,
                                'user': DoctorSerializers(doctor).data,
                                'work_hours': WorkingHourSerializers(work_hours, many=True).data,
                                'education': EducationDetailsSerializers(education, many=True).data,
                                'certificates': CertificateSerializers(certificates, many=True).data,
                                'academic_field': AcademicFieldSerializers(academic_field, many=True).data
                            },
                            status=200
                        )
            return get_Response(
                success=False,
                message='کاربری یافت نشد ',
                status=401
            )

        return get_Response(
            success=True,
            message='خطایی رخ داده است',
            status=404
        )

    def patch(self, request):
        if request.user and request.user.is_authenticated:
            if user := User.objects.filter(phone_number=request.user).first():
                print('the user')
                if user.is_doctor == True:
                    print('the doctor')
                    print("Request Data:", request.data)
                    doctor = DoctorModel.objects.filter(user=user).first()
                    if educationId := request.data.get('edit_edu'):
                        print('hi')
                        print(educationId)
                        if education := EducationDetailsModel.objects.filter(id=educationId, doctor=doctor).first():
                            print('eduaction get')
                            education_serializers = EducationDetailsSerializers(instance=education,
                                                                                data=request.data, partial=True)
                            print('hi 3')
                            if education_serializers.is_valid():
                                print('ok')
                                education_serializers.save()
                                print('serializer is save!')
                                return get_Response(
                                    success=True,
                                    status=200,
                                    message='رکورد تحصیللات با موفقیت ویرایش شد',
                                    data=education_serializers.data,
                                )
                            if not education_serializers.is_valid():
                                print("Doctor serializer errors:", education_serializers.errors)
                    user_data = {
                        "first_name": request.data.get('first_name'),
                        "last_name": request.data.get("last_name"),
                        "birthday": request.data.get("birthday"),
                        "bio": request.data.get("bio")
                    }
                    user_serializer = UserSerializers(data=user_data, instance=user, partial=True)
                    if user_serializer.is_valid():
                        user_serializer.save()
                    srz = DoctorSerializers(data=request.data, instance=doctor, partial=True)
                    if srz.is_valid():
                        srz.save()

                        updated_data = DoctorSerializers(instance=doctor).data
                        updated_data['user'] = UserSerializers(instance=user).data

                        return get_Response(
                            success=True,
                            message='the doctor profile is updated ',
                            status=200,
                            data=updated_data
                        )
                    if not srz.is_valid():
                        return get_Response(
                            success=False,
                            message='داده های ارسال شده معتبر نیست',
                            status=500,
                            data=srz.errors
                        )

                else:
                    srz = self.serializer_class(data=request.data, instance=user, partial=True)
                    if srz.is_valid():
                        srz.save()
                        return get_Response(
                            success=True,
                            message='the user profile is updated ',
                            status=200,
                            data=srz.data
                        )

            return get_Response(
                success=False,
                message='the user is not found',
                status=404,
            )

        return get_Response(
            success=False,
            message='unauthorized',
            status=500
        )

    def put(self, request):
        max_upload_size = 10 * 1024 * 1024  # 10MB
        max_size = 150 * 1024  # 150KB

        if request.user and request.user.is_authenticated:
            print('authenticated')
            if user := User.objects.filter(phone_number=request.user).first():
                if user.is_doctor == True:
                    print('is doctor!!')
                    if doctor := DoctorModel.objects.filter(user=user).first():
                        print('doctor found')
                        if image := request.FILES.get('image'):
                            print('the image is here')
                            print(image.size)
                            if image.size > max_upload_size:
                                return get_Response(
                                    success=False,
                                    status=400,
                                    message='the image is longer than 10 Mb'
                                )
                            if image.size > max_size:
                                image = compress_image(image)
                            if doctor.image:
                                print('last image is delete')
                                doctor.image.delete()
                            doctor.image = image
                            doctor.save()
                            return get_Response(
                                success=True,
                                status=200,
                                message='the image profile is success',
                                data={'image_url': doctor.image.url}
                            )
                        return get_Response(
                            success=False,
                            status=400,
                            message='the serializers is not valid',
                        )
                return get_Response(
                    success=False,
                    status=400,
                    message='the doctor is not found',
                )

            return get_Response(
                success=False,
                status=400,
                message='the user is not valid',
            )

        return get_Response(
            success=False,
            status=401,
            message='the authenticated faild',
        )

    def delete(self, request):
        if request.user and request.user.is_authenticated:
            if user := User.objects.filter(pk=request.user.id).first():
                if user.is_doctor:
                    doctor = DoctorModel.objects.filter(user__id=user.id).first()
                    working_hour_id = request.query_params.get("working_hour_id")
                    education_id = request.query_params.get("education_id")
                    certificate_id = request.query_params.get("certificate_id")
                    if working_hour_id:
                        if works_hours := WorkingHourModel.objects.filter(pk=working_hour_id, doctor=doctor).first():
                            works_hours.delete_record = 'WAITING'
                            works_hours.save()
                            return get_Response(
                                success=True,
                                message='رکورد در انتظار حذف توسط ادمین',
                                status=200
                            )
                    elif education_id:
                        if educations := EducationDetailsModel.objects.filter(pk=education_id, doctor=doctor).first():
                            educations.delete()
                            return get_Response(
                                success=True,
                                status=200,
                                message='رکورد تحصیللات با موفقیت حذف شد'
                            )
                    elif certificate_id:
                        if certificate := get_object_or_404(CertificateModel, pk=certificate_id, doctor=doctor):
                            certificate.delete()
                            return get_Response(
                                success=True,
                                status=200,
                                message='گواهینامه مورد نظر حذف شد'
                            )
        return get_Response(
            success=False,
            message='خطا در حذف رکورد',
            status=400
        )

    def post(self, request):
        if not request.user or not request.user.is_authenticated:
            return get_Response(success=False, message='لاگین کنید', status=401)

        user = User.objects.filter(pk=request.user.id).first()
        if not user:
            return get_Response(success=False, message='کاربر مورد نظر یافت نشد', status=400)

        if not user.is_doctor:
            return get_Response(success=False, message='شما دسترسی لازم را ندارید', status=401)

        doctor = DoctorModel.objects.filter(user__id=user.id).first()
        if not doctor:
            return get_Response(success=False, message='دکتر یافت نشد', status=400)

        schedules = request.data.get('schedules', [])  # دریافت لیست برنامه‌های کاری
        educations = request.data.get('Educations', [])  # دریافت لیست تحصیلا
        print(educations)
        if schedules:  # بررسی اینکه `schedules` مقدار داشته باشد
            if not isinstance(schedules, list):
                print('no')
                return get_Response(success=False, message='فرمت داده‌های برنامه کاری اشتباه است', status=400)

            srz = WorkingHourSerializers(data=schedules, many=True, context={'doctor': doctor})
            print('hi')
            if srz.is_valid():
                srz.save()
                return get_Response(
                    success=True,
                    message='داده‌های شما ثبت شد',
                    status=200,
                    data=srz.data
                )

            return get_Response(success=False, message='خطا در سریالایز کردن داده‌های برنامه کاری', status=400,
                                data=srz.errors)

        elif educations:  # اگر `schedules` مقدار نداشت، ولی `educations` مقدار داشته باشد
            print('hoo')
            if not isinstance(educations, list):
                return get_Response(success=False, message='فرمت داده‌های تحصیلات اشتباه است', status=400)

            print('hiiiii education')
            srz = EducationDetailsSerializers(data=educations, many=True, context={'doctor': doctor})
            if srz.is_valid():
                print('hi')
                srz.save()
                return get_Response(
                    success=True,
                    message='رکورد تحصیلات با موفقیت ثبت شد',
                    status=200,
                    data=srz.data
                )

            return get_Response(success=False, message='خطا در سریالایز کردن داده‌های تحصیلات', status=400,
                                data=srz.errors)

        return get_Response(success=False, message='هیچ داده‌ای ارسال نشده است', status=400)


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


class LogoutApi(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return get_Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    success=False,
                    message='Refresh token is required'
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': 'User logged out successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginApi(APIView):
    def post(self, request):
        token = request.data.get('token')
        idinfo = id_token.verify_oauth2_token(token, requests.Request(),
                                              "971156426829-l5np1sfkm6hbu3ku2i1glbia08t0udte.apps.googleusercontent.com", )
        email = idinfo['email']
        first_name = idinfo['given_name']
        last_name = idinfo['family_name']
        user, created = User.objects.get_or_create(email=email, defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        })
        tokens = create_jwt_user(user)
        return get_Response(
            success=True,
            message='وورد یا ثبت نام با موفقیت انجام شد',
            tokens=tokens,
            status=status.HTTP_200_OK
        )
