from django.db import models
from django.core.validators import RegexValidator
import random


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

password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&+])[A-Za-z\d@$!%*#?&+]{8,}$"
password_validator = RegexValidator(
    regex=password_regex,
    message="Мінімум вісім символів, одна літера, одна цифра та один спеціальний символ: @ $ ! % * # ? & +",
    code='invalid_password'
)
card_regex = r"^\d{4} \d{4} \d{4} \d{4}$"
card_validator = RegexValidator(
    regex=card_regex,
    message="Номер картки записується у вигляді хххх хххх хххх хххх",
    code='invalid_card'
)
passport_regex = r'^[1-9]\d{9}$'
passport_validator = RegexValidator(
    regex=passport_regex,
    message="Номер паспорта не починається з 0 та містить 10 символів",
    code='invalid_passport'
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
    customer_name = models.CharField('Ім\'я', validators=[name_validator], max_length=30)
    customer_surname = models.CharField('Прізвище', validators=[name_validator], max_length=30)
    customer_middle_name = models.CharField('По-батькові', validators=[name_validator], max_length=30)
    customer_city = models.CharField('Місто', validators=[name_validator], max_length=30)
    customer_address = models.CharField('Вулиця', validators=[name_validator], max_length=30)
    customer_number_of_house = models.IntegerField('Номер будинку')
    customer_phone_number = models.CharField('Телефон', validators=[phone_validator], max_length=17)
    customer_email = models.EmailField('Пошта', unique=True, max_length=100)
    customer_passport_code = models.IntegerField('Код паспорту', unique=True, validators=[passport_validator])
    customer_date_of_birth = models.DateField('День народження')
    customer_password = models.CharField('Пароль', validators=[password_validator], max_length=40)
    customer_credit_card = models.CharField('Номер кредитної карти', validators=[card_validator], unique=True, max_length=19)

    def save(self, *args, **kwargs):
        self.customer_name = self.customer_name.capitalize()
        self.customer_surname = self.customer_surname.capitalize()
        self.customer_middle_name = self.customer_middle_name.capitalize()
        self.customer_city = self.customer_city.capitalize()
        self.customer_address = self.customer_address.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer_name}  {self.customer_surname}  {self.customer_middle_name}'

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

    def __str__(self):
        return f'{self.type}'

    class Meta:
        app_label = 'catalog'


class Receipt(models.Model):
    PAYMENT = (
        ('Готівка', 'Готівка'),
        ('Безготівковий розрахунок', 'Безготівковий розрахунок'),
    )
    DELIVERY = (
        ('Кур\'єрська доставка', 'Кур\'єрська доставка'),
        ('Термінова кур\'єрська доставка', 'Термінова кур\'єрська доставка'),
        ('Штатний кур\'єр', 'Штатний кур\'єр'),
        ('Самовивіз із офісу', 'Самовивіз із офісу'),
        ('Постамати', 'Постамати'),
        ('Пошта України', 'Пошта України'),
    )
    id_receipt = models.AutoField(primary_key=True)
    id_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, verbose_name='Товар', unique=True)
    id_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупець')
    number_of_receipt = models.IntegerField('Номер чеку', null=True, blank=True)
    date_of_purchase = models.DateTimeField('Дата покупки')
    the_item_cost = models.FloatField('Вартість товару', null=True, blank=True)
    method_of_delivery = models.CharField('Тип доставки', choices=DELIVERY, max_length=30)
    payment_type = models.CharField('Тип оплати', choices=PAYMENT, max_length=30)

    def save(self, *args, **kwargs):
        if self.id_item:
            self.the_item_cost = self.id_item.price
        if not self.number_of_receipt:
            matching_receipt = Receipt.objects.filter(
                id_customer=self.id_customer,
                date_of_purchase=self.date_of_purchase,
                method_of_delivery=self.method_of_delivery,
                payment_type=self.payment_type
            ).first()
            if matching_receipt:
                self.number_of_receipt = matching_receipt.number_of_receipt
            else:
                self.number_of_receipt = random.randint(1, 1000000)
                while Receipt.objects.filter(number_of_receipt=self.number_of_receipt).exists():
                    self.number_of_receipt = random.randint(1, 1000000)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.number_of_receipt}'

    class Meta:
        app_label = 'catalog'



