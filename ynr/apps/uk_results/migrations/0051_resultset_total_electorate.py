# Generated by Django 2.2.18 on 2021-04-30 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("uk_results", "0050_candidateresult_tied_vote_winner")]

    operations = [
        migrations.AddField(
            model_name="resultset",
            name="total_electorate",
            field=models.PositiveIntegerField(blank=True, null=True),
        )
    ]
