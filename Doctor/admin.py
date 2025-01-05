from typing import Any
import requests
from django.contrib import admin
from django import forms
from django_jalali import forms as jforms
from django.core.exceptions import ValidationError
from dal import autocomplete

from Doctor.models import *
from Accounts.models import User
from utils.book_apoointment import get_available_slots


class DoctorModelForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=25, required=True)
    last_name = forms.CharField(label='Last Name', max_length=55, required=True)
    phone_number = forms.CharField(label='Phone Number', max_length=11, required=True)
    is_active = forms.BooleanField(label='is_Active')
    birthday = jforms.jDateField(widget=forms.DateInput(attrs={'type': 'date'}))
    is_doctor = forms.BooleanField(label='is_doctor')


    class Meta:
        model = DoctorModel
        fields = ['image','first_name', 'last_name', 'phone_number', 'is_active', 'birthday','bio','landline_phone','medical_license_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            print('User instance found')
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['phone_number'].initial = self.instance.user.phone_number
            self.fields['is_active'].initial = self.instance.user.is_active
            self.fields['birthday'].initial = self.instance.user.birthday
            self.fields['is_doctor'].initial = self.instance.user.is_doctor
        else:
            print('No user instance found')

    def save(self, commit=True):
        doctor_instance = super().save(commit=False)
        # if not doctor_instance.user:
        user = doctor_instance.user or User()
        # elif doctor_instance.user:
        #     user = doctor_instance.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.birthday = self.cleaned_data.get('birthday')
        user.is_active = self.cleaned_data.get('is_active')
        user.is_doctor = True
        user.save()
        # if not doctor_instance:
        doctor_instance.user = user
        if commit:
            doctor_instance.save()
        return doctor_instance

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # بررسی اینکه شماره تلفن فعلی همان شماره تلفن قبلی است
        if self.instance.user:
            existing_user = User.objects.filter(phone_number=phone_number).exclude(id=self.instance.user.id)
        else:
            existing_user = User.objects.filter(phone_number=phone_number)

        if existing_user.exists():
            raise forms.ValidationError('شماره تلفن وارد شده قبلاً ثبت شده است.')

        return phone_number


class AppointmentAdminForm(forms.ModelForm):
    class Meta:
        model = AppointmentModel
        fields = ('doctor', 'patient', 'time', 'date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = User.object.filter(is_doctor=False)
        
        
    def clean(self):
        cleaned_data = super().clean()
        doctor_id = self.cleaned_data.get('doctor')
        patient_id = self.cleaned_data.get('user')
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')
        try:
            get_available_slots(doctor=doctor_id,patient=patient_id,date=date,time=time)
            
        except ValidationError as e:
            print(e.message)
            raise forms.ValidationError(e.message)
        
        return cleaned_data
        


class CertificateStackedInline(admin.StackedInline):
    model = CertificateModel
    list_display = (
        'doctor', 'certificate_name', 'issuing_institution', 'date_issue', 'expiration_date', 'additional_details')
    extra = 0


class EducationModelAdminForm(forms.ModelForm):
    # country = forms.ChoiceField(choices=EducationDetailsModel.choices_country(), required=True)
    # university = forms.ChoiceField(choices=EducationDetailsModel.choices_uni(), required=True)

    class Media:
        js = ('js/adminPanel.js',)

    class Meta:
        model = EducationDetailsModel
        fields = ('doctor', 'academic_field', 'country', 'university', 'graduation_year')


@admin.register(EducationDetailsModel)
class EducationDetailsModelAdmin(admin.ModelAdmin):
    form = EducationModelAdminForm
    list_display = ('academic_field', 'university', 'graduation_year', 'doctor')


class EducationDetailsModelStackedInlineAdmin(admin.StackedInline):
    class Media:
        js = ('js/adminPanel.js',)

    model = EducationDetailsModel
    form = EducationModelAdminForm
    list_display = ('academic_field', 'university', 'graduation_year', 'doctor')
    extra = 0


class WorkingHourModelStackedInline(admin.StackedInline):
    model = WorkingHourModel
    extra = 1


@admin.register(DoctorModel)
class DoctorModelAdmin(admin.ModelAdmin):
    form = DoctorModelForm
    inlines = [CertificateStackedInline, EducationDetailsModelStackedInlineAdmin, WorkingHourModelStackedInline]
    # list_display = (' ',)


@admin.register(MedicalSpecialtyModel)
class MedicalSpecialtyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'description')


class DetailsMedicalSpecialtyForm(forms.ModelForm):
    class Meta:
        model = DetailsMedicalSpecialty
        fields = '__all__'
        widgets = {
            'specialty': autocomplete.ModelSelect2(
                url='specialty-autocomplete',
                forward=['doctor']
            )
        }


@admin.register(DetailsMedicalSpecialty)
class DetailsMedicalSpecialtyAdmin(admin.ModelAdmin):
    form = DetailsMedicalSpecialtyForm



        
                
    


@admin.register(AppointmentModel)
class AppointmentModelAdmin(admin.ModelAdmin):
    form = AppointmentAdminForm
    # fields = ('doctor', 'patient', 'date', 'time')
    list_display = ('date', 'time')
    
    
@admin.register(DoctorDepartmentModel)
class DepartmentModelAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'image')


admin.site.register(CertificateModel)
admin.site.register(WorkingHourModel)
