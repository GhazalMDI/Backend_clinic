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
            send_code(Random_code,phone_number)

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
