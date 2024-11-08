from django.contrib import admin
from Accounts.models import User


# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'phone_number', 'is_active', 'birthday')

