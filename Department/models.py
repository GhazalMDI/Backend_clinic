from django.db import models


# from Doctor.models import DoctorModel


class DepartmentModel(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='department/', null=True, blank=True)
    # department = models.ForeignKey('Department.DepartmentModel', related_name='department_medical_special',on_delete=models.PROTECT)


    def __str__(self):
        return self.title
