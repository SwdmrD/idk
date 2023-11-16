from django.db import models


class Fabric(models.Model):
    DESTINY = (
        ('high', 'Висока'),
        ('moderate', 'Помірна'),
        ('average', 'Середня'),
        ('low', 'Низька'),
        ('different', 'Різна'),
    )
    ELASTICITY = (
        ('non-elastic', 'Не еластична'),
        ('almost non-elastic', 'Майже не еластична'),
        ('partially elastic', 'Частково еластична'),
        ('highly elastic', 'Добре еластична')
    )

    BREATHABILITY = (
        ('low', 'Низька'),
        ('almost absent', 'Майже відсутня'),
        ('medium', 'Середня'),
        ('high', 'Висока')
    )

    TEXTURE = (
        ('glossy', 'Блискуча'),
        ('geometric', 'Геометрична'),
        ('smooth', 'Гладка'),
        ('textured', 'Гофрована'),
        ('diagonal', 'Діагональна'),
        ('matte', 'Матова'),
        ('embossed', 'Рельєфна'),
        ('ribbed', 'Рубчаста'),
        ('mesh', 'Сітчаста'),
        ('complex', 'Складна'),
        ('striped', 'Смужкова'),
        ('rough', 'Шорстка')
    )

    RESISTANCE = (
        ('high resistance', 'Висока стійкість'),
        ('medium resistance', 'Середня стійкість'),
        ('low resistance', 'Низька стійкість'),
        ('anti-compression fabric', 'Антикомпресійна тканина')
    )

    FASTNESS = (
        ('high fastness', 'Висока стійкість'),
        ('medium fastness', 'Середня стійкість'),
        ('low fastness', 'Низька стійкість'),
        ('unknown', 'Невідомо')
    )
    id_fabric = models.AutoField(primary_key=True)
    fabric_name = models.CharField('Назва тканини', max_length=30)
    destiny = models.CharField('Щільність', max_length=30, choices=DESTINY)
    elasticity = models.CharField('Еластичність', max_length=30, choices=ELASTICITY)
    breathability = models.CharField('Повітропроникність', max_length=30, choices=BREATHABILITY)
    surface_texture = models.CharField('Текстура', max_length=30, choices=TEXTURE)
    compression_resistance = models.CharField('Стійкість до стиснення', max_length=30, choices=RESISTANCE)
    color_fastness = models.CharField('Стійкість кольору', max_length=30, choices=FASTNESS)

    def __str__(self):
        return self.fabric_name

    class Meta:
        app_label = 'catalog'


class Supplier(models.Model):
    id_supplier = models.AutoField(primary_key=True)
    company_name = models.CharField('Назва компанії', max_length=50)
    contact_person_name = models.CharField('Ім\'я контактної персони', max_length=50)
    contact_person_surname = models.CharField('Прізвище контактної персони', max_length=50)
    phone_number = models.CharField('Телефон', max_length=16)
    city = models.CharField('Місто', max_length=50)
    email = models.EmailField('Пошта', max_length=100)

    def __str__(self):
        return self.company_name

    class Meta:
        app_label = 'catalog'


class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True)
    name = models.CharField('Ім\'я', max_length=30)
    surname = models.CharField('Прізвище', max_length=30)
    middle_name = models.CharField('По-батькові', max_length=30)
    city = models.CharField('Місто', max_length=30)
    address = models.CharField('Вулиця', max_length=30)
    number_of_house = models.CharField('Номер будинку', max_length=30)
    phone_number = models.CharField('Телефон', max_length=16)
    email = models.EmailField('Пошта', max_length=100)
    passport_code = models.CharField('Код паспорту', max_length=10)
    date_of_birth = models.DateField('День народження')
    password = models.CharField('Пароль', max_length=40)
    credit_cars = models.CharField('Номер кредитної карти', max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'catalog'


class Receipt(models.Model):
    id_receipt = models.AutoField(primary_key=True)
    id_item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='receipts')
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_of_purchase = models.DateTimeField('Дата покупки')
    the_total_cost = models.FloatField('Загальна вартість')
    method_of_delivery = models.CharField('Тип', max_length=30)
    payment_type = models.CharField('Тип', max_length=30)

    def __str__(self):
        return f'{self.date_of_purchase} - {self.id_customer} - {self.id_receipt}'

    class Meta:
        app_label = 'catalog'


class Item(models.Model):
    SIZE = (
        ('xxs', 'XXS'),
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XXL'),
        ('xxl', 'XXL')
    )
    TREATMENT = (
        ('not processed', 'Не оброблено'),
        ('needs chemical treatment', 'Потребує хімічної обробки'),
        ('treated with light chemistry', 'Оброблено легкою хімією'),
        ('treated with heavy chemicals', 'Оброблено важкою хімією'),
        ('treated with anti-allergic agents', 'Оброблено протиалергічними засобами')
    )
    SEASONALITY = (
        ('winter', 'Зима'),
        ('spring', 'Весна'),
        ('summer', 'Літо'),
        ('autumn', 'Осінь'),
        ('demi-season', 'Демісезон'),
        ('all', 'Любий'),
    )
    COLOR = (
        ('beige', 'Бежевий'),
        ('white', 'Білий'),
        ('blue', 'Блакитний'),
        ('burgundy', 'Бордовий'),
        ('yellow', 'Жовтий'),
        ('green', 'Зелений'),
        ('brown', 'Коричневий'),
        ('orange', 'Помаранчевий'),
        ('pink', 'Рожевий'),
        ('blue', 'Синій'),
        ('gray', 'Сірий'),
        ('red', 'Червоний'),
        ('black', 'Чорний'),
        ('purple', 'Фіолетовий'),
        ('other color', 'Інші кольори'),
        ('multicolored', 'Різнокольоровий'),
        ('print', 'Принт'),
    )
    CHOICE = (
        ('true', 'Так'),
        ('false', 'Ні')
    )
    GENDER = (
        ('female', 'Жіночій'),
        ('male', 'Чоловічий'),
        ('unisex', 'Унісекс')
    )
    id_item = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, verbose_name='Постачальник')
    fabric = models.ForeignKey(Fabric, on_delete=models.SET_NULL, null=True, verbose_name='Тканина')
    type = models.CharField('Тип', max_length=30)
    brand = models.CharField('Бренд', max_length=30)
    size = models.CharField('Розмір', max_length=30,choices=SIZE)
    gender = models.CharField('Приналежність', max_length=30,choices=GENDER)
    color = models.CharField('Колір', max_length=30,choices=COLOR)
    chemical_treatment = models.CharField('Хімічна обробка', max_length=100, choices=TREATMENT)
    state = models.CharField('Стан', max_length=100)
    seasonality = models.CharField('Сезонність', max_length=100, choices=SEASONALITY)
    price = models.FloatField('Ціна')
    date_of_appearance = models.DateTimeField("Дата появи товару")
    sold_or_not = models.CharField('Наявність', choices=CHOICE,  max_length=10, default=False)

    def __str__(self):
        return f'{self.type} - {self.supplier} - {self. fabric}'

    class Meta:
        app_label = 'catalog'


