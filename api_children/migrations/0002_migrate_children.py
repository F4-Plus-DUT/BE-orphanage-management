# Generated by Django 4.1 on 2022-09-21 14:44

from django.db import migrations

from api_children.static import ChildrenData


def init_data_children(apps, schema_editor):
    children_model = apps.get_model("api_children", "Children")
    children = [children_model(name=children['name'], gender=children['gender'], age=children['age'],
                               personal_picture=children['personal_picture']) for children in ChildrenData.children]
    children_model.objects.bulk_create(children)


class Migration(migrations.Migration):
    dependencies = [
        ('api_children', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_data_children, migrations.RunPython.noop)
    ]
