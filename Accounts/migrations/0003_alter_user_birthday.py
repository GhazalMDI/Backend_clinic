# Generated by Django 5.1.2 on 2024-11-01 07:39

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=django_jalali.db.models.jDateField(null=True),
        ),
    ]
