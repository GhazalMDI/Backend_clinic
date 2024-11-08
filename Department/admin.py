from django.contrib import admin
from Department.models import *


@admin.register(DepartmentModel)
class DepartmentModelAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'image')
