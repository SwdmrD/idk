# Generated by Django 4.2.5 on 2023-11-15 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0032_rename_supplier_item_id_supplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='id_supplier',
            new_name='supplier',
        ),
    ]
