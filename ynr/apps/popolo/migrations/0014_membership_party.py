# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-03 13:46
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parties", "0003_party_ordering"),
        ("popolo", "0013_clean_up_after_postextra_move"),
    ]

    operations = [
        migrations.AddField(
            model_name="membership",
            name="party",
            field=models.ForeignKey(
                help_text="The political party for this membership",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="parties.Party",
            ),
        )
    ]
