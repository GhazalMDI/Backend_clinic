import requests
from django.contrib import admin
from django import forms
from django_jalali import forms as jforms
from django.core.exceptions import ValidationError

from Doctor.models import *
from Accounts.models import User


class DoctorModelForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=25, required=True)
    last_name = forms.CharField(label='Last Name', max_length=55, required=True)
    phone_number = forms.CharField(label='Phone Number', max_length=11, required=True)
    is_active = forms.BooleanField(label='is_Active')
    birthday = jforms.jDateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = DoctorModel
        fields = ['image', 'department', 'first_name', 'last_name', 'phone_number', 'is_active', 'birthday']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            print('User instance found')
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['phone_number'].initial = self.instance.user.phone_number
            self.fields['is_active'].initial = self.instance.user.is_active
            self.fields['birthday'].initial = self.instance.user.birthday
        else:
            print('No user instance found')

    def save(self, commit=True):
        doctor_instance = super().save(commit=False)
        if not doctor_instance.user:
            user = User()
        elif doctor_instance.user:
            user = doctor_instance.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.birthday = self.cleaned_data.get('birthday')
        user.is_active = self.cleaned_data.get('is_active')
        user.save()
        if not doctor_instance:
            doctor_instance.user = user
        if commit:
            doctor_instance.save()
        return doctor_instance

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.object.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('لطفا شماره تلفن صحیح وارد نمایید')
        return phone_number


class CertificateStackedInline(admin.StackedInline):
    model = CertificateModel
    list_display = (
        'doctor', 'certificate_name', 'issuing_institution', 'date_issue', 'expiration_date', 'additional_details')
    extra = 1


class EducationModelAdminForm(forms.ModelForm):
    country = forms.ChoiceField(choices=EducationDetailsModel.choices_country(), required=True)
    university = forms.ChoiceField(choices=EducationDetailsModel.choices_uni(), required=True)

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
    extra = 1


@admin.register(DoctorModel)
class DoctorModelAdmin(admin.ModelAdmin):
    form = DoctorModelForm
    inlines = [CertificateStackedInline, EducationDetailsModelStackedInlineAdmin]


@admin.register(MedicalSpecialtyModel)
class MedicalSpecialtyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'description')


@admin.register(DetailsMedicalSpecialty)
class DetailsMedicalSpecialtyAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'years_of_experience', 'description')


admin.site.register(CertificateModel)
