from rest_framework import serializers
from Doctor.models import *


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = DoctorModel
        fields = '__all__'


class DoctorSerializers(serializers.ModelSerializer):
    department = DepartmentSerializers(many=True)

    class Meta:
        model = DoctorModel
        fields = '__all__'
