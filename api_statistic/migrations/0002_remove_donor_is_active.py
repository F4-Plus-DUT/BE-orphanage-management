# Generated by Django 4.1 on 2022-10-04 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_statistic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donor',
            name='is_active',
        ),
    ]