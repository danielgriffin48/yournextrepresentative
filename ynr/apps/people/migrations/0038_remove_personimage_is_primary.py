# Generated by Django 3.2.4 on 2022-02-16 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("people", "0037_alter_personimage_person")]

    operations = [
        migrations.RemoveField(model_name="personimage", name="is_primary")
    ]
