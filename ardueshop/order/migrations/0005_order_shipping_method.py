# Generated by Django 4.2.7 on 2023-12-06 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_merge_20231205_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_method',
            field=models.CharField(choices=[('Entrega estándar', 'Entrega estándar'), ('Recogida en tienda', 'Recogida en tienda')], default='Entrega estándar', max_length=25),
        ),
    ]
