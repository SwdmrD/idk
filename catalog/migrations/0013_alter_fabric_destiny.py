# Generated by Django 4.2.5 on 2023-10-19 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_fabric_destiny'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabric',
            name='destiny',
            field=models.CharField(choices=[('default', 'Висока'), ('default1', 'Помірна'), ('default2', 'Середня'), ('default3', 'Низька'), ('default5', 'Різна')], default='Висока', max_length=30, verbose_name='Щільність'),
        ),
    ]
