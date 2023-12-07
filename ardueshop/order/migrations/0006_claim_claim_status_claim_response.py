# Generated by Django 4.2.7 on 2023-12-06 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='claim_status',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Atendida', 'Atendida')], default='Pendiente', max_length=20),
        ),
        migrations.AddField(
            model_name='claim',
            name='response',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
