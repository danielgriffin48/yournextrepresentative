# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-23 19:54
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("people", "0004_move_person_data")]

    operations = [
        migrations.AlterField(
            model_name="personimage",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="people.Person",
            ),
        )
    ]
