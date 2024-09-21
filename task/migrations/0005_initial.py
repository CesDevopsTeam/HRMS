# Generated by Django 5.0.6 on 2024-09-18 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Attendance', '0006_delete_task'),
        ('task', '0004_delete_taskassign'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_description', models.TextField(verbose_name='Task Description')),
                ('assigned_at', models.DateTimeField(auto_now_add=True, verbose_name='Assigned At')),
                ('is_acknowledged', models.BooleanField(default=False, verbose_name='Acknowledged')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='Attendance.employeepersonalinfo')),
            ],
        ),
    ]
