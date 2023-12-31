# Generated by Django 4.2.5 on 2023-10-18 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_fabric_breathability_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=100, verbose_name='Пошта'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='breathability',
            field=models.CharField(choices=[('default', 'Низька'), ('default1', 'Майже відсутня'), ('default2', 'Середня'), ('default3', 'Висока')], default='Низька', max_length=30, verbose_name='Повітропроникність'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='color_fastness',
            field=models.CharField(choices=[('default', 'Висока стійкість'), ('default1', 'Середня стійкість'), ('default2', 'Низька стійкість'), ('default3', 'Спеціалізована стійкість'), ('default4', 'Фарбована'), ('default5', 'Невідомо')], default='Висока стійкість', max_length=30, verbose_name='Стійкість кольору'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='compression_resistance',
            field=models.CharField(choices=[('default', 'Висока стійкість'), ('default1', 'Середня стійкість'), ('default2', 'Низька стійкість'), ('default3', 'Антикомпресійна тканина')], default='Висока стійкість', max_length=30, verbose_name='Стійкість до стиснення'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='destiny',
            field=models.CharField(choices=[('default', 'Висока'), ('default1', 'Помірна'), ('default2', 'Середня'), ('default3', 'Низька'), ('default5', 'Різна')], default='Висока', max_length=30, verbose_name='Щільність'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='elasticity',
            field=models.CharField(choices=[('default', 'Не еластична'), ('default1', 'Майже не еластична'), ('default2', 'Частоково еластична'), ('default3', 'Добре еластична')], default='Не еластична', max_length=30, verbose_name='Еластичність'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='surface_texture',
            field=models.CharField(choices=[('default', 'Блискуча'), ('default1', 'Геометрична'), ('default2', 'Гладка'), ('default3', 'Гофрована'), ('default4', 'Діагональна'), ('default5', 'Матова'), ('default6', 'Рельєфна'), ('default7', 'Рубчаста'), ('default8', 'Сітчаста'), ('default9', 'Складна'), ('default10', 'Смужкова'), ('default11', 'Шорстка')], default='Блискуча', max_length=30, verbose_name='Текстура'),
        ),
        migrations.AlterField(
            model_name='item',
            name='receipt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.receipt'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='id_customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.customer'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='id_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to='catalog.item'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='email',
            field=models.EmailField(max_length=100, verbose_name='Пошта'),
        ),
    ]
