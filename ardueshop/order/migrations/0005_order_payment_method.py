# Generated by Django 4.2.7 on 2023-12-05 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_merge_20231205_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Tarjeta', 'Tarjeta'), ('Contra-reembolso', 'Contra-reembolso')], default='Tarjeta', max_length=20),
            preserve_default=False,
        ),
    ]
