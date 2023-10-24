# Generated by Django 4.2.5 on 2023-10-24 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_alter_item_color_alter_item_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='address',
            new_name='city',
        ),
        migrations.AlterField(
            model_name='item',
            name='fabric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.fabric', verbose_name='Тканина'),
        ),
        migrations.AlterField(
            model_name='item',
            name='state',
            field=models.CharField(max_length=100, verbose_name='Стан'),
        ),
        migrations.AlterField(
            model_name='item',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.supplier', verbose_name='Постачальник'),
        ),
    ]
