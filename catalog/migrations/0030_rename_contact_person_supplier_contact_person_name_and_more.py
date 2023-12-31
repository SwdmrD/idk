# Generated by Django 4.2.5 on 2023-11-14 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0029_alter_item_fabric_alter_item_supplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='contact_person',
            new_name='contact_person_name',
        ),
        migrations.AlterField(
            model_name='item',
            name='fabric',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.fabric', verbose_name='Тканина'),
        ),
    ]
