# Generated by Django 5.1.4 on 2024-12-05 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_otpmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otpmodel',
            name='user',
        ),
    ]
