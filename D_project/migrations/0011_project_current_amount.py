# Generated by Django 5.0.3 on 2024-03-07 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('D_project', '0010_merge_0009_comment_0009_donation_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='current_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
