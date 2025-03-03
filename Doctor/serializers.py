from rest_framework import serializers

from Doctor.models import *
from Accounts.serializers import UserSerializers


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = DoctorDepartmentModel
        fields = ('title', 'image', 'description')


class DoctorSerializers(serializers.ModelSerializer):
    # department = DepartmentSerializers()
    user = UserSerializers()

    class Meta:
        model = DoctorModel
        fields = ('user', 'image', 'landline_phone', 'medical_license_number', 'bio')


class AcademicFieldSerializers(serializers.ModelSerializer):
    class Meta:
        model = AcademicFieldModel
        fields = '__all__'


class EducationDetailsSerializers(serializers.ModelSerializer):
    academic_field = AcademicFieldSerializers()
    doctor = DoctorSerializers()

    class Meta:
        model = EducationDetailsModel
        fields = '__all__'


class CertificateSerializers(serializers.ModelSerializer):
    doctor = DoctorSerializers()

    class Meta:
        model = CertificateModel
        fields = '__all__'


class MedicalSpecialtySerializers(serializers.ModelSerializer):
    department = DepartmentSerializers(many=True, read_only=True)

    class Meta:
        model = MedicalSpecialtyModel
        fields = '__all__'


class DetailsMedicalSerializers(serializers.ModelSerializer):
    specialty = MedicalSpecialtySerializers(many=True)
    doctor = DoctorSerializers(many=True, read_only=True)

    class Meta:
        model = DetailsMedicalSpecialty
        fields = '__all__'


class WorkingHourSerializers(serializers.ModelSerializer):
    class Meta:
        model = WorkingHourModel
        fields = ('id', 'doctor', 'day', 'start_time', 'end_time')

    DAYS_MAPPING = {
        ('5', 'شنبه'),
        ('6', 'یکشنبه'),
        ('0', 'دوشنبه'),
        ('1', 'سه شنبه'),
        ('2', 'چهارشنبه'),
        ('3', 'پنجشنبه'),
        ('4', 'جمعه')
    }

    doctor = DoctorSerializers(read_only=True)

    def validated_day(self, value):
        print('validated day')
        if value in self.DAYS_MAPPING:
            return self.DAYS_MAPPING[value]
        elif value in dict(WorkingHourModel.DAYS).keys():
            return value
        raise serializers.ValidationError("مقدار نامعتبر برای روز")

    def create(self, validated_data):
        doctor = self.context.get('doctor')
        if not doctor:
            raise serializers.ValidationError({'doctor': 'دکتر مشخص نشده است'})
        w = WorkingHourModel.objects.create(doctor=doctor, **validated_data)
        print(f'ID==== {w.id}')
        return w




class AppointmentSerializers(serializers.ModelSerializer):
    doctor = DoctorSerializers(read_only=True)
    patient = UserSerializers(read_only=True)

    class Meta:
        model = AppointmentModel
        fields = '__all__'
