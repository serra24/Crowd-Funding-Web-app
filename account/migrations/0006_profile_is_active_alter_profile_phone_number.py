# Generated by Django 5.0.3 on 2024-04-18 03:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Phone number must start with 01 and be 9 digits long.', regex='^01\\d{9}$')]),
        ),
    ]