# Generated by Django 5.1.2 on 2024-11-22 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0031_workinghourmodel_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workinghourmodel',
            name='end',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='workinghourmodel',
            name='start',
            field=models.TimeField(),
        ),
    ]
