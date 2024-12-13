from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, first_name=None, last_name=None,email=None, birthday=None):
        if not phone_number:
            raise ValidationError('لطفا شماره تلفن معتبر وارد نمایید')
        user = self.model(
            phone_number=phone_number, first_name=first_name, last_name=last_name,email=email, birthday=birthday
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, first_name=None, last_name=None,email=None, birthday=None):
        user = self.create_user(phone_number, password, first_name, last_name,email, birthday)
        user.is_admin = True
        user.save(using=self._db)
        return user
