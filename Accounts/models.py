from django.db import models
from django_jalali.db import models as jmodel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from Accounts.manager import UserManager
from Doctor.models import DoctorModel


class User(AbstractBaseUser):
    phone_number = models.CharField(unique=True,max_length=11)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=55)
    birthday = jmodel.jDateField(null=True)
    national_code = models.CharField(max_length=10,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['last_name', 'first_name']
    object = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    def is_staff(self):
        return self.is_admin

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.last_name} {self.last_name}'
        if not self.first_name and self.last_name:
            return f'{self.last_name}'
        if self.first_name and not self.last_name:
            return f'{self.last_name}'
        return 'کاربر عزیز'


