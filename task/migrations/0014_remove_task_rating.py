# Generated by Django 5.0.6 on 2024-09-22 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_task_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='rating',
        ),
    ]
