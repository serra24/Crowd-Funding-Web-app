# Generated by Django 3.2.12 on 2024-03-07 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
