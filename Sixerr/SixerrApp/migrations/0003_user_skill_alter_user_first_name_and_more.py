# Generated by Django 5.1.6 on 2025-02-27 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SixerrApp', '0002_remove_user_is_admin_remove_user_is_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='skill',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='John', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='Smith', max_length=255),
        ),
    ]
