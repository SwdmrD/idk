# Generated by Django 4.2.5 on 2023-11-24 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0049_alter_customer_customer_passport_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='the_item_cost',
            field=models.IntegerField(default='1', verbose_name='Номер чеку'),
            preserve_default=False,
        ),
    ]
