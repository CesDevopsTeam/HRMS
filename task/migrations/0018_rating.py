# Generated by Django 5.0.6 on 2024-09-20 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0006_delete_task'),
        ('task', '0017_alter_task_assigned_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(verbose_name='Rating Score')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Rating Date')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='Attendance.employeepersonalinfo')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='task.task')),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Ratings',
                'unique_together': {('task', 'employee')},
            },
        ),
    ]
