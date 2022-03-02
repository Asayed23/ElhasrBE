# Generated by Django 3.2 on 2022-03-01 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20220301_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
