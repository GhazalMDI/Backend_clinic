# Generated by Django 5.1.2 on 2024-11-23 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0030_doctormodel_days_doctormodel_end_doctormodel_start'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctormodel',
            old_name='DAYS',
            new_name='days',
        ),
    ]
