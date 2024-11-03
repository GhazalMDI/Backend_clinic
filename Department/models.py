from django.db import models
from Doctor.models import DoctorModel


class Department(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    doctors = models.ForeignKey('Doctor.DoctorModel', models.SET_NULL, 'department_doctors', null=True, blank=True)
    image = models.ImageField(upload_to='department/')

    def __str__(self):
        return self.title
