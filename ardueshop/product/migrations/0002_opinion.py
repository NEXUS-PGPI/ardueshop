# Generated by Django 4.2.7 on 2023-11-25 15:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2023, 11, 25, 15, 47, 13, 795463, tzinfo=datetime.timezone.utc))),
                ('comment', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opinions', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opinions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
