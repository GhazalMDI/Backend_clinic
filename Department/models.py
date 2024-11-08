from django.db import models


# from Doctor.models import DoctorModel


class DepartmentModel(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='department/', null=True, blank=True)

    def __str__(self):
        return self.title
