import requests
from django.db import models

from Department.models import DepartmentModel


class DoctorModel(models.Model):
    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
    user = models.OneToOneField('Accounts.User', on_delete=models.CASCADE, related_name='doctor_profile', null=True,
                                blank=True)
    department = models.ForeignKey('Department.DepartmentModel', models.SET_NULL, 'department_doctors', null=True,
                                   blank=True)
    landline_phone = models.CharField(max_length=11, null=True)
    medical_license_number = models.CharField(max_length=5, null=True)
    bio = models.TextField(null=True)


class EducationDetailsModel(models.Model):
    academic_field = models.ForeignKey('AcademicFieldModel', models.PROTECT, null=True, blank=True,
                                       related_name='academic_to_education')
    university = models.CharField(max_length=255, null=True)
    graduation_year = models.IntegerField(null=True)
    doctor = models.ForeignKey('DoctorModel', related_name='doctor_education', on_delete=models.PROTECT, null=True)

    # def __str__(self):
    #     return self.academic_field

    country = models.CharField(max_length=150, null=True)

    @classmethod
    def choices_country(cls):
        url = 'https://countriesnow.space/api/v0.1/countries/positions'
        res = requests.get(url)
        countries = res.json()
        countries_choices = [(c['name'], c['name']) for c in countries['data']]
        return countries_choices

    @classmethod
    def choices_uni(cls):
        url = 'https://raw.githubusercontent.com/Hipo/university-domains-list/refs/heads/master/world_universities_and_domains.json'
        response = requests.get(url)
        universities = response.json()
        university_choices = [(uni['name'], uni['name']) for uni in universities if uni.get('country') == 'Iran']
        return university_choices


class AcademicFieldModel(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
