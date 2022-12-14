# Generated by Django 4.1 on 2022-11-04 15:07

import base.models.fields
import dirtyfields.dirtyfields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api_user', '0007_migrate_employee'),
        ('api_activity', '0007_alter_activity_end_date_alter_activity_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdoptRequestDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('income', models.CharField(blank=True, max_length=235, null=True)),
                ('marital_status', base.models.fields.TinyIntegerField(choices=[(1, 'Single'), (2, 'Married'), (3, 'Other')], default=1)),
                ('family_status', models.BooleanField(default=0)),
                ('adopter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adopter', to='api_user.profile')),
            ],
            options={
                'db_table': 'adopt_request_details',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='adoptrequest',
            name='adopter',
        ),
        migrations.RemoveField(
            model_name='adoptrequest',
            name='form_detail',
        ),
        migrations.CreateModel(
            name='Proof',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('link', models.CharField(blank=True, default='', max_length=255)),
                ('adopt_request_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proof', to='api_activity.adoptrequestdetail')),
            ],
            options={
                'db_table': 'proofs',
                'ordering': ('created_at',),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='adoptrequest',
            name='adopt_request_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adopt_request_detail', to='api_activity.adoptrequestdetail'),
        ),
    ]
