from django.contrib import admin
from Accounts.models import User, AddressModel, OtpModel


# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'phone_number', 'is_active', 'birthday', 'is_doctor')
    list_display = ('first_name', 'last_name', 'phone_number', 'is_active', 'birthday', 'is_doctor')
    list_filter = ('is_doctor', 'is_admin')


@admin.register(AddressModel)
class AddressAdmin(admin.ModelAdmin):
    fields = ('formatted_address', 'state', 'county', 'neighbourhood')
    list_display = ('formatted_address', 'state', 'county', 'neighbourhood')


@admin.register(OtpModel)
class OtpModelAdmin(admin.ModelAdmin):
    fields = ('phone_number','random_code', 'created')
    list_display = ('phone_number', 'random_code', 'created')
