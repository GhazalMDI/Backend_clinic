from django.shortcuts import render
from rest_framework.views import APIView

from Department.models import DepartmentModel
from Department.serializers import DepartmentSerializers
from rest_framework.response import Response


class DepartmentDetailsApiView(APIView):

    def get(self, request, d_id):
        departments = DepartmentModel.objects.all()
        if d_id:
            department = departments.filter(id=d_id).first()
            dsrz = DepartmentSerializers(department, many=False)
            return Response({
                'data': dsrz.data
            })
        else:
            return Response({
                'message': 'the department_id is undefined'
            })
