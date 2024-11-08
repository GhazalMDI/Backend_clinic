from rest_framework import serializers
from Department.models import *


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = DepartmentModel
        fields = '__all__'
