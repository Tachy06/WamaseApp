# Generated by Django 5.0.1 on 2024-04-23 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SystemLogin', '0003_moreinformation_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moreinformation',
            name='brand',
        ),
    ]
