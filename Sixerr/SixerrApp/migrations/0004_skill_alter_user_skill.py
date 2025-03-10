# Generated by Django 5.1.6 on 2025-03-10 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SixerrApp', '0003_user_skill_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('skill_name', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='skill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SixerrApp.skill'),
        ),
    ]
