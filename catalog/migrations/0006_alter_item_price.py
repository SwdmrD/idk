# Generated by Django 4.2.5 on 2023-10-04 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_customer_city_alter_customer_credit_cars_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(verbose_name='Ціна'),
        ),
    ]
