import requests
from django.db import models
from django_jalali.db import models as jmodel

from Department.models import DepartmentModel


# from Accounts.models import User


class DoctorModel(models.Model):
    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
    user = models.OneToOneField('Accounts.User', on_delete=models.CASCADE, related_name='doctor_profile', null=True,
                                blank=True)
    department = models.ForeignKey('Department.DepartmentModel', models.SET_NULL, 'department_doctors', null=True,
                                   blank=True)
    landline_phone = models.CharField(max_length=11, null=True)
    medical_license_number = models.CharField(max_length=5, null=True)
    bio = models.TextField(null=True)


    def __str__(self):
        if self.user and self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        return 'دکتر'


class EducationDetailsModel(models.Model):
    academic_field = models.ForeignKey('AcademicFieldModel', models.PROTECT, null=True, blank=True,
                                       related_name='academic_to_education')
    university = models.CharField(max_length=255, null=True)
    graduation_year = models.IntegerField(null=True)
    doctor = models.ForeignKey('DoctorModel', related_name='doctor_education', on_delete=models.PROTECT, null=True)
    country = models.CharField(max_length=150, null=True)

    # @classmethod
    # def choices_country(cls):
    #     try:
    #         res = requests.get('https://restcountries.com/v3.1/all')
    #         res.raise_for_status()  # Raise HTTPError for bad responses
    #         countries = [(country['cca2'], country['name']['common']) for country in res.json()]
    #         return countries
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error fetching country data: {e}")
    #         return []


    # @classmethod
    # def choices_uni(cls):
    #     url = 'https://raw.githubusercontent.com/Hipo/university-domains-list/refs/heads/master/world_universities_and_domains.json'
    #     response = requests.get(url)
    #     universities = response.json()
    #     university_choices = [(uni['name'], uni['name']) for uni in universities]
    #     return university_choices


class AcademicFieldModel(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class CertificateModel(models.Model):
    doctor = models.ForeignKey('DoctorModel', models.PROTECT, 'certificate_doctor')
    certificate_name = models.CharField(max_length=155)
    issuing_institution = models.CharField(max_length=255)
    date_issue = jmodel.jDateField()
    expiration_date = jmodel.jDateField(null=True, blank=True)
    additional_details = models.TextField()


class MedicalSpecialtyModel(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey('Department.DepartmentModel', related_name='department_medical_special',
                                   on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class DetailsMedicalSpecialty(models.Model):
    specialty = models.ForeignKey('MedicalSpecialtyModel', related_name='Details_Medical_Specialty_related',
                                  on_delete=models.SET_NULL, null=True)
    years_of_experience = jmodel.jDateField()
    description = models.TextField(null=True, blank=True)
    doctor = models.ForeignKey('DoctorModel', models.PROTECT, 'doctor_medical_specialty')


class WorkingHourModel(models.Model):
    DAYS = (
        ('5', 'شنبه'),
        ('6', 'یکشنبه'),
        ('0', 'دوشنبه'),
        ('1', 'سه شنبه'),
        ('2', 'چهارشنبه'),
        ('3', 'پنجشنبه'),
        ('4', 'جمعه')
    )

    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, related_name='doctor_working_hours')
    day = models.CharField(max_length=15, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()


class AppointmentModel(models.Model):
    doctor = models.ForeignKey('DoctorModel', related_name='doctor_appointment', on_delete=models.PROTECT)
    patient = models.ForeignKey('Accounts.User', related_name='patient_appointment', on_delete=models.PROTECT,null=True)
    date = jmodel.jDateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)

    # def __str__(self):
    #     return f'{self.doctor.user.full_name}-{self.patient.first_name} {self.patient.last_name}-{self.date}-{self.time}'




