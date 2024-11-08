# Generated by Django 5.1.2 on 2024-11-03 08:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_alter_user_birthday'),
        ('Doctor', '0014_remove_doctormodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to='Doctor.doctormodel'),
        ),
    ]
