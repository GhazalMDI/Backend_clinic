from django.db import models
from Department.models import DepartmentModel


class DoctorModel(models.Model):
    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
    user = models.OneToOneField('Accounts.User', on_delete=models.CASCADE, related_name='doctor_profile', null=True,
                                blank=True)
    department = models.ForeignKey('Department.DepartmentModel', models.SET_NULL, 'department_doctors', null=True,
                                   blank=True)
