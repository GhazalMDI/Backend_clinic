# Generated by Django 5.1.4 on 2025-03-06 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0003_alter_certificatemodel_additional_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='workinghourmodel',
            name='add_record',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='workinghourmodel',
            name='delete_record',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
