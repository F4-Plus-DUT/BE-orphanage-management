# Generated by Django 4.1 on 2022-09-27 17:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_children', '0003_remove_children_adopt_date_remove_children_adopter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='children',
            name='join_date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 9, 28, 0, 32, 28, 901906), null=True),
        ),
    ]
