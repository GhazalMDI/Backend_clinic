from Accounts.models import User
from Doctor.models import DoctorModel, EducationDetailsModel, WorkingHourModel, CertificateModel, AcademicFieldModel
from Doctor.serializers import (
    UserSerializers, DoctorSerializers, EducationDetailsSerializers,
    WorkingHourSerializers, CertificateSerializers, AcademicFieldSerializers
)
from utils.StandardResponse import get_Response


class ProfileHandler:

    @staticmethod
    def get_profile(user):
        if not user or not user.is_authenticated:
            return get_Response(success=False, message='Unauthorized', status=401)

        db_user = User.objects.filter(phone_number=user).first()
        if not db_user:
            return get_Response(success=False, message='کاربری یافت نشد', status=404)

        if not db_user.is_doctor:
            return get_Response(
                success=True,
                message='به پروفایل خوش آمدید',
                data={'status_doctor': False, 'user': UserSerializers(db_user).data},
                status=200
            )

        doctor = DoctorModel.objects.filter(user=db_user).first()
        if not doctor:
            return get_Response(success=False, message='Doctor not found', status=404)

        work_hours = WorkingHourModel.objects.filter(doctor=doctor)
        education = EducationDetailsModel.objects.filter(doctor=doctor)
        certificates = CertificateModel.objects.filter(doctor=doctor)
        academic_field = AcademicFieldModel.objects.all()

        return get_Response(
            success=True,
            message='دکتر گرامی به پروفایل خوش آمدید',
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

    @staticmethod
    def update_profile(user, data):
        db_user = User.objects.filter(phone_number=user).first()
        if not db_user:
            return get_Response(success=False, message='کاربر یافت نشد', status=404)

        if db_user.is_doctor:
            doctor = DoctorModel.objects.filter(user=db_user).first()
            user_serializer = UserSerializers(instance=db_user, data=data, partial=True)
            doctor_serializer = DoctorSerializers(instance=doctor, data=data, partial=True)

            if user_serializer.is_valid(): user_serializer.save()
            if doctor_serializer.is_valid():
                doctor_serializer.save()
                return get_Response(success=True, message='پروفایل دکتر بروزرسانی شد',
                                    data=doctor_serializer.data, status=200)

            return get_Response(success=False, message='خطا در بروزرسانی پروفایل', data=doctor_serializer.errors, status=400)

        else:
            srz = UserSerializers(instance=db_user, data=data, partial=True)
            if srz.is_valid():
                srz.save()
                return get_Response(success=True, message='پروفایل کاربر بروزرسانی شد', data=srz.data, status=200)

            return get_Response(success=False, message='داده نامعتبر است', data=srz.errors, status=400)

    @staticmethod
    def create_schedule_or_education(user, data):
        db_user = User.objects.filter(pk=user.id).first()
        if not db_user or not db_user.is_doctor:
            return get_Response(success=False, message='شما دسترسی لازم را ندارید', status=403)

        doctor = DoctorModel.objects.filter(user=db_user).first()
        if not doctor:
            return get_Response(success=False, message='دکتر یافت نشد', status=404)

        schedules = data.get('schedules', [])
        educations = data.get('Educations', [])

        if schedules:
            srz = WorkingHourSerializers(data=schedules, many=True, context={'doctor': doctor})
            if srz.is_valid():
                srz.save()
                return get_Response(success=True, message='برنامه کاری ثبت شد', data=srz.data, status=201)
            return get_Response(success=False, message='خطا در داده‌های برنامه کاری', data=srz.errors, status=400)

        if educations:
            srz = EducationDetailsSerializers(data=educations, many=True, context={'doctor': doctor})
            if srz.is_valid():
                srz.save()
                return get_Response(success=True, message='تحصیلات ثبت شد', data=srz.data, status=201)
            return get_Response(success=False, message='خطا در داده‌های تحصیلات', data=srz.errors, status=400)

        return get_Response(success=False, message='هیچ داده‌ای ارسال نشده است', status=400)
