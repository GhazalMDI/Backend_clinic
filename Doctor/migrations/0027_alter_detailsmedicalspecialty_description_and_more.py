# Generated by Django 5.1.2 on 2024-11-16 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0026_detailsmedicalspecialty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailsmedicalspecialty',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medicalspecialtymodel',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]