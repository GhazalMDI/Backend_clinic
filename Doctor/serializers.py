from rest_framework import serializers

from Doctor.models import *
from Accounts.serializers import UserSerializers


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = DoctorModel
        fields = '__all__'


class DoctorSerializers(serializers.ModelSerializer):
    department = DepartmentSerializers(many=True)
    user = UserSerializers(many=True, read_only=True)

    class Meta:
        model = DoctorModel
        fields = '__all__'


class AcademicFieldSerializers(serializers.ModelSerializer):
    class Meta:
        model = AppointmentModel
        fields = '__all__'


class EducationDetailsSerializers(serializers.ModelSerializer):
    academic_field = AcademicFieldSerializers(many=True, read_only=True)

    class Meta:
        model = EducationDetailsModel
        fields = '__all__'
