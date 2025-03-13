# Generated by Django 5.1.6 on 2025-03-11 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SixerrApp', '0008_skill_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='images/users/default.jpg', upload_to='images/users/'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='image',
            field=models.ImageField(default='images/skills/default.jpg', upload_to='images/skills/'),
        ),
    ]
