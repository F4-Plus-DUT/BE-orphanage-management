# Generated by Django 4.1 on 2022-09-09 05:51

import base.models.fields
import dirtyfields.dirtyfields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api_user', '0003_migrate_admin_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('gender', base.models.fields.TinyIntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')])),
                ('birthday', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(max_length=11, null=True, validators=[django.core.validators.RegexValidator(message='A valid integer is required.', regex='^\\d+$'), django.core.validators.MinLengthValidator(9)])),
            ],
            options={
                'db_table': 'users',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='account',
            name='role',
        ),
        migrations.AddField(
            model_name='account',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='account',
            name='roles',
            field=models.ManyToManyField(null=True, related_name='users', to='api_user.role'),
        ),
        migrations.AddField(
            model_name='role',
            name='last_modified_by',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='role',
            name='scope_text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='profile',
            name='account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]