# Generated by Django 4.2.9 on 2024-09-13 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_leaverequest_approved_by_leaverequest_approved_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Is Approved'),
        ),
        migrations.AddField(
            model_name='leaverequest',
            name='remark',
            field=models.TextField(blank=True, null=True, verbose_name='Remark'),
        ),
    ]
