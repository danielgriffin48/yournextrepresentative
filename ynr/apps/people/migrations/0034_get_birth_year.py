# Generated by Django 3.2.4 on 2021-10-27 14:41

from django.db import migrations


def get_birth_year(apps, schema_editor):
    Person = apps.get_model("people", "Person")
    for person in Person.objects.exclude(birth_date="").iterator():
        birth_year = person.birth_date.split("-")[0]
        person.birth_date = birth_year
        person.save()


class Migration(migrations.Migration):

    dependencies = [("people", "0033_auto_20210928_1007")]

    operations = [
        migrations.RunPython(get_birth_year, migrations.RunPython.noop)
    ]
