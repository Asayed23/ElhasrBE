# Generated by Django 3.1.6 on 2022-03-17 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20220317_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='modified_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]