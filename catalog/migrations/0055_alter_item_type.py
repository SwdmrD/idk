# Generated by Django 4.2.5 on 2023-12-03 20:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0054_remove_item_date_of_appearance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='invalid_name', message='Використовуйте українську мову.', regex="^[А-ЩЬЮЯҐЄІЇа-щьюяґєії\\'\\s]+$")], verbose_name='Тип'),
        ),
    ]
