# Generated by Django 4.2.5 on 2023-09-30 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_item_item_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='size',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
