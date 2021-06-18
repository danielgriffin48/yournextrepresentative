# Generated by Django 2.2.20 on 2021-06-17 14:06

from django.db import migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [("candidates", "0069_ballot_voting_system")]

    operations = [
        migrations.AlterModelOptions(
            name="ballot",
            options={
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
            },
        ),
        migrations.AddField(
            model_name="ballot",
            name="created",
            field=django_extensions.db.fields.CreationDateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ballot",
            name="modified",
            field=django_extensions.db.fields.ModificationDateTimeField(
                auto_now=True, verbose_name="modified"
            ),
        ),
    ]
