# Generated by Django 5.1.2 on 2024-11-03 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Department', '0009_remove_departmentmodel_doctors'),
        ('Doctor', '0015_doctormodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctormodel',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_doctors', to='Department.departmentmodel'),
        ),
    ]
