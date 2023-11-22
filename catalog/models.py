from django.db import models
from django.core.validators import RegexValidator


name_regex = r'^[А-ЩЬЮЯҐЄІЇа-щьюяґєії\'\s]+$'
name_validator = RegexValidator(
    regex=name_regex,
    message="Використовуйте українську мову.",
    code='invalid_name'
)

phone_regex = r"^\+380 \d{2}-\d{3}-\d{2}-\d{2}$"
phone_validator = RegexValidator(
    regex=phone_regex,
    message="Номер телефона повинен бути у форматі: '+380 12-345-67-89'.",
    code='invalid_phone_number'
)



class Fabric(models.Model):
    DESTINY = (
        ('Висока', 'Висока'),
        ('Помірна', 'Помірна'),
        ('Середня', 'Середня'),
        ('Низька', 'Низька'),
        ('Різна', 'Різна'),
    )
    ELASTICITY = (
        ('Не еластична', 'Не еластична'),
        ('Майже не еластична', 'Майже не еластична'),
        ('Частково еластична', 'Частково еластична'),
        ('Добре еластична', 'Добре еластична')
    )

    BREATHABILITY = (
        ('Низька', 'Низька'),
        ('Майже відсутня', 'Майже відсутня'),
        ('Середня', 'Середня'),
        ('Висока', 'Висока')
    )

    TEXTURE = (
        ('Блискуча', 'Блискуча'),
        ('Гладка', 'Гладка'),
        ('Гофрована', 'Гофрована'),
        ('Діагональна', 'Діагональна'),
        ('Матова', 'Матова'),
        ('М\'яка', 'М\'яка'),
        ('Рельєфна', 'Рельєфна'),
        ('Рубчаста', 'Рубчаста'),
        ('Сітчаста', 'Сітчаста'),
        ('Складна', 'Складна'),
        ('Смужкова', 'Смужкова'),
        ('Шорстка', 'Шорстка')
    )

    RESISTANCE = (
        ('Висока стійкість', 'Висока стійкість'),
        ('Середня стійкість', 'Середня стійкість'),
        ('Низька стійкість', 'Низька стійкість'),
        ('Антикомпресійна тканина', 'Антикомпресійна тканина')
    )

    FASTNESS = (
        ('Висока стійкість', 'Висока стійкість'),
        ('Середня стійкість', 'Середня стійкість'),
        ('Низька стійкість', 'Низька стійкість'),
        ('Невідомо', 'Невідомо')
    )
    id_fabric = models.AutoField(primary_key=True)
    fabric_name = models.CharField('Назва тканини', validators=[name_validator], unique=True, max_length=30)
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
    company_name = models.CharField('Назва компанії',unique=True, max_length=50)
    contact_person_name = models.CharField('Ім\'я контактної персони', validators=[name_validator], max_length=50)
    contact_person_surname = models.CharField('Прізвище контактної персони',validators=[name_validator], max_length=50)
    phone_number = models.CharField('Телефон', validators=[phone_validator], unique=True, max_length=17)
    city = models.CharField('Місто', validators=[name_validator], max_length=50)
    email = models.EmailField('Пошта', unique=True, max_length=100)

    def save(self, *args, **kwargs):
        self.contact_person_name = self.contact_person_name.capitalize()
        self.contact_person_surname = self.contact_person_surname.capitalize()
        self.city = self.city.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name

    class Meta:
        app_label = 'catalog'


class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True)
    name = models.CharField('Ім\'я', validators=[name_validator], max_length=30)
    surname = models.CharField('Прізвище', validators=[name_validator], max_length=30)
    middle_name = models.CharField('По-батькові', validators=[name_validator], max_length=30)
    city = models.CharField('Місто', validators=[name_validator], max_length=30)
    address = models.CharField('Вулиця', validators=[name_validator], max_length=30)
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
        ('xl', 'XL'),
        ('xxl', 'XXL')
    )
    TREATMENT = (
        ('Не оброблено', 'Не оброблено'),
        ('Потребує хімічної обробки', 'Потребує хімічної обробки'),
        ('Оброблено легкою хімією', 'Оброблено легкою хімією'),
        ('Оброблено важкою хімією', 'Оброблено важкою хімією'),
        ('Оброблено протиалергічними засобами', 'Оброблено протиалергічними засобами')
    )

    SEASONALITY = (
        ('Зима', 'Зима'),
        ('Весна', 'Весна'),
        ('Літо', 'Літо'),
        ('Осінь', 'Осінь'),
        ('Демісезон', 'Демісезон'),
        ('Любий', 'Любий'),
    )

    COLOR = (
        ('Бежевий', 'Бежевий'),
        ('Білий', 'Білий'),
        ('Блакитний', 'Блакитний'),
        ('Бордовий', 'Бордовий'),
        ('Жовтий', 'Жовтий'),
        ('Зелений', 'Зелений'),
        ('Коричневий', 'Коричневий'),
        ('Помаранчевий', 'Помаранчевий'),
        ('Рожевий', 'Рожевий'),
        ('Синій', 'Синій'),
        ('Сірий', 'Сірий'),
        ('Червоний', 'Червоний'),
        ('Чорний', 'Чорний'),
        ('Фіолетовий', 'Фіолетовий'),
        ('Інші кольори', 'Інші кольори'),
        ('Різнокольоровий', 'Різнокольоровий'),
        ('Принт', 'Принт'),
    )

    GENDER = (
        ('Жіночій', 'Жіночій'),
        ('Чоловічий', 'Чоловічий'),
        ('Унісекс', 'Унісекс')
    )

    STATE = (
        ('Є значні дефекти', 'Є значні дефекти'),
        ('Є незначні дефекти', 'Є незначні дефекти'),
        ('Трішки ношений', 'Трішки ношений'),
        ('Новий', 'Новий'),
    )
    id_item = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, verbose_name='Постачальник')
    fabric = models.ForeignKey(Fabric, on_delete=models.SET_NULL, null=True, verbose_name='Тканина')
    type = models.CharField('Тип', max_length=30)
    brand = models.CharField('Бренд', max_length=30)
    size = models.CharField('Розмір', max_length=30,choices=SIZE)
    gender = models.CharField('Приналежність', max_length=30, choices=GENDER)
    color = models.CharField('Колір', max_length=30, choices=COLOR)
    chemical_treatment = models.CharField('Хімічна обробка', max_length=100, choices=TREATMENT)
    seasonality = models.CharField('Сезонність', max_length=100, choices=SEASONALITY)
    state = models.CharField('Стан', max_length=100, choices=STATE)
    price = models.FloatField('Ціна')
    date_of_appearance = models.DateField("Дата появи товару")

    def save(self, *args, **kwargs):
        self.type = self.type.capitalize()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.type} - {self.supplier} - {self. fabric}'

    class Meta:
        app_label = 'catalog'


