# Generated by Django 4.2.7 on 2023-11-25 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_opinion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 15, 47, 44, 527018, tzinfo=datetime.timezone.utc)),
        ),
    ]
