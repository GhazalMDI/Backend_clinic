from rest_framework import serializers

from Doctor.models import *
from Accounts.serializers import UserSerializers


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = DoctorModel
        fields = '__all__'


class DoctorSerializers(serializers.ModelSerializer):
    department = DepartmentSerializers()
    user = UserSerializers(read_only=True)

    class Meta:
        model = DoctorModel
        fields = '__all__'


class AcademicFieldSerializers(serializers.ModelSerializer):
    class Meta:
        model = AppointmentModel
        fields = '__all__'


class EducationDetailsSerializers(serializers.ModelSerializer):
    academic_field = AcademicFieldSerializers(many=True, read_only=True)
    doctor = DoctorSerializers(many=True, read_only=True)

    class Meta:
        model = EducationDetailsModel
        fields = '__all__'


class CertificateSerializers(serializers.ModelSerializer):
    doctor = DoctorSerializers(many=True, read_only=True)

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
    doctor = DoctorSerializers(many=True, read_only=True)

    class Meta:
        model = WorkingHourModel
        fields = '__all__'


class AppointmentSerializers(serializers.ModelSerializer):
    doctor = DoctorSerializers( read_only=True)
    patient = UserSerializers( read_only=True)

    class Meta:
        model = AppointmentModel
        fields = '__all__'
