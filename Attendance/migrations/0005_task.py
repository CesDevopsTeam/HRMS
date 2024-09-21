# Generated by Django 5.0.6 on 2024-09-18 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0004_remove_employeesalarydeduction_lwf_amt_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=70)),
                ('password', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'task',
            },
        ),
    ]
