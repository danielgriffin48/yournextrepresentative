# Generated by Django 2.2.4 on 2019-11-13 20:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("people", "0017_set_vandalism_list")]

    operations = [
        migrations.CreateModel(
            name="GenderGuess",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("gender", models.CharField(max_length=1)),
                (
                    "person",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gender_guess",
                        to="people.Person",
                    ),
                ),
            ],
        )
    ]
