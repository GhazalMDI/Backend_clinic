from django.db import models


class DoctorModel(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11, unique=True)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.last_name} {self.last_name}'
        if not self.first_name and self.last_name:
            return f'{self.last_name}'
        if self.first_name and not self.last_name:
            return f'{self.last_name}'
        return 'دکتر عزیز'
