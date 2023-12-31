# Generated by Django 4.2.5 on 2023-11-22 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0043_alter_customer_customer_credit_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='id_customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.customer', verbose_name='Покупець'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='id_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.item', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='method_of_delivery',
            field=models.CharField(choices=[("Кур'єрська доставка", "Кур'єрська доставка"), ("Термінова кур'єрська доставка", "Термінова кур'єрська доставка"), ("Штатний кур'єр", "Штатний кур'єр"), ('Самовивіз із офісу', 'Самовивіз із офісу'), ('Постамати', 'Постамати'), ('Пошта України', 'Пошта України')], max_length=30, verbose_name='Тип доставки'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='payment_type',
            field=models.CharField(choices=[('Готівка', 'Готівка'), ('Безготівковий розрахунок', 'Безготівковий розрахунок')], max_length=30, verbose_name='Тип оплати'),
        ),
    ]
