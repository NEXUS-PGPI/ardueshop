# Generated by Django 4.2.7 on 2023-12-05 11:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0003_alter_opinion_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="opinion",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 12, 5, 11, 25, 20, 500617, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
