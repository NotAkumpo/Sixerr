# Generated by Django 5.1.6 on 2025-04-05 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SixerrApp', '0013_user_bio_user_join_date_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='join_date',
        ),
    ]
