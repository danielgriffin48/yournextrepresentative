# Generated by Django 3.2.4 on 2021-09-29 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("facebook_data", "0003_auto_20210401_0811")]

    operations = [
        migrations.AlterField(
            model_name="facebookadvert",
            name="ad_json",
            field=models.JSONField(
                help_text="The JSON returned from the Facebook Graph API for this advert"
            ),
        )
    ]
