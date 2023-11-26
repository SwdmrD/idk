# Generated by Django 4.2.5 on 2023-11-24 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0052_alter_receipt_the_item_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='number_of_receipt',
            field=models.IntegerField(unique=True, verbose_name='Номер чеку'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='the_item_cost',
            field=models.FloatField(blank=True, null=True, verbose_name='Вартість товару'),
        ),
    ]
