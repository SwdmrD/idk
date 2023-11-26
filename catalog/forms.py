from .models import Item, Fabric, Supplier, Customer, Receipt
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from datetime import date, timedelta, datetime
import datetime as dt
import pytz
import random
from django.db.models.signals import pre_save


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        widgets = {
            'date_of_appearance': forms.DateInput(attrs={'type': 'date', 'placeholder': 'дд.мм.рррр'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and (price < 0 or price > 5000):
            raise ValidationError('Неправильна ціна, можливий діапазон від 0 до 5000')
        return round(price, 2)

    def clean_date_of_appearance(self):
        date_of_appearance = self.cleaned_data.get('date_of_appearance')

        if date_of_appearance and date_of_appearance > date.today() + timedelta(days=1):
            raise ValidationError('Дата не може бути у майбутньому')

        return date_of_appearance


class ItemForm2(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and (price < 0 or price > 5000):
            raise ValidationError('Неправильна ціна, можливий діапазон від 0 до 5000')
        return round(price, 2)

    def clean_date_of_appearance(self):
        date_of_appearance = self.cleaned_data.get('date_of_appearance')

        if date_of_appearance and date_of_appearance > date.today() + timedelta(days=1):
            raise ValidationError('Дата не може бути у майбутньому')

        return date_of_appearance


class FabricForm(ModelForm):
    class Meta:
        model = Fabric
        fields = "__all__"


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            'customer_phone_number': forms.TextInput(attrs={'placeholder': '+380 xx-ххх-хх-хх'}),
            'customer_credit_card': forms.TextInput(attrs={'placeholder': 'хxхх хххх хххх хххх'}),
            'customer_date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'дд.мм.рррр'}),
        }

    def clean_customer_number_of_house(self):
        customer_number_of_house = self.cleaned_data.get('customer_number_of_house')
        if customer_number_of_house and (customer_number_of_house < 1 or customer_number_of_house > 500):
            raise ValidationError('Введіть номер будинку від 1 до 500')
        return customer_number_of_house

    def clean_customer_date_of_birth(self):
        customer_date_of_birth = self.cleaned_data.get('customer_date_of_birth')
        if customer_date_of_birth:
            current_date = datetime.now(pytz.UTC)
            age = current_date.year - customer_date_of_birth.year
            if age < 18 or age > 100:
                raise ValidationError('Невірна дата народження')
        return customer_date_of_birth


class CustomerForm2(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            'customer_phone_number': forms.TextInput(attrs={'placeholder': '+380 xx-ххх-хх-хх'}),
            'customer_credit_card': forms.TextInput(attrs={'placeholder': 'хxхх хххх хххх хххх'}),
        }

    def clean_customer_number_of_house(self):
        customer_number_of_house = self.cleaned_data.get('customer_number_of_house')
        if customer_number_of_house and (customer_number_of_house < 1 or customer_number_of_house > 500):
            raise ValidationError('Введіть номер будинку від 1 до 500')
        return customer_number_of_house

    def clean_customer_date_of_birth(self):
        customer_date_of_birth = self.cleaned_data.get('customer_date_of_birth')
        if customer_date_of_birth:
            current_date = datetime.now(pytz.UTC)
            age = current_date.year - customer_date_of_birth.year
            if age < 18 or age > 100:
                raise ValidationError('Невірна дата народження')
        return customer_date_of_birth


class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = "__all__"
        widgets = {
            'date_of_purchase': forms.DateInput(attrs={'type': 'datetime-local', 'placeholder': 'дд.мм.рррр'}),
            'the_item_cost': forms.HiddenInput(),
            'number_of_receipt': forms.HiddenInput(),
        }

    def clean_date_of_purchase(self):
        date_of_purchase = self.cleaned_data.get('date_of_purchase')
        if date_of_purchase:
            current_date = dt.datetime.now(pytz.UTC)
            min_date = datetime(2023, 1, 1, 00, 00, 00, tzinfo=pytz.UTC)
            if date_of_purchase >= current_date or date_of_purchase <= min_date:
                raise ValidationError('Дата покупки не може бути більшою за '
                                      'сьогодніщній день та меншою ніж 01.01.2023')
        return date_of_purchase


class ReceiptForm2(ModelForm):
    class Meta:
        model = Receipt
        fields = "__all__"
        widgets = {
            'the_item_cost': forms.HiddenInput(),
        }

    def clean_date_of_purchase(self):
        date_of_purchase = self.cleaned_data.get('date_of_purchase')
        if date_of_purchase:
            current_date = datetime.now(pytz.UTC)
            min_date = datetime(2023, 1, 1, 00, 00, 00, tzinfo=pytz.UTC)
            if date_of_purchase >= current_date or date_of_purchase <= min_date:
                raise ValidationError('Дата покупки не може бути більшою за '
                                      'сьогодніщній день та меншою ніж 01.01.2023')
        return date_of_purchase


class FabricFilterForm(forms.Form):
    destiny = forms.MultipleChoiceField(
        label='Щільність',
        choices=Fabric.DESTINY,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    elasticity = forms.MultipleChoiceField(
        label='Еластичність',
        choices=Fabric.ELASTICITY,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    breathability = forms.MultipleChoiceField(
        label='Повітропроникність',
        choices=Fabric.BREATHABILITY,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    surface_texture = forms.MultipleChoiceField(
        label='Текстура',
        choices=Fabric.TEXTURE,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    compression_resistance = forms.MultipleChoiceField(
        label='Стійкість до стиснення',
        choices=Fabric.RESISTANCE,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    color_fastness = forms.MultipleChoiceField(
        label='Стійкість кольору',
        choices=Fabric.FASTNESS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class SupplierFilterForm(forms.Form):
    contact_person_name = forms.MultipleChoiceField(
        label='Ім\'я контактної персони',
        choices=[(x['contact_person_name'], x['contact_person_name']) for x in Supplier.objects.values('contact_person_name').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    contact_person_surname = forms.MultipleChoiceField(
        label='Прізвище контактної персони',
        choices=[(x['contact_person_surname'], x['contact_person_surname']) for x in Supplier.objects.values('contact_person_surname').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    phone_number = forms.MultipleChoiceField(
        label='Телефон',
        choices=[(x['phone_number'], x['phone_number']) for x in Supplier.objects.values('phone_number').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    city = forms.MultipleChoiceField(
        label='Місто',
        choices=[(x['city'], x['city']) for x in Supplier.objects.values('city').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    email = forms.MultipleChoiceField(
        label='Пошта',
        choices=[(x['email'], x['email']) for x in Supplier.objects.values('email').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class ItemFilterForm(forms.Form):
    brand = forms.MultipleChoiceField(
        label='Бренд',
        choices=[(x['brand'], x['brand']) for x in Item.objects.values('brand').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    size = forms.MultipleChoiceField(
        label='Розмір',
        choices=Item.SIZE,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    gender = forms.MultipleChoiceField(
        label='Приналежність',
        choices=Item.GENDER,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    color = forms.MultipleChoiceField(
        label='Колір',
        choices=Item.COLOR,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    fabric = forms.MultipleChoiceField(
        label = 'Тканина',
        choices = [(x.id_fabric, x.fabric_name) for x in Fabric.objects.all()],
        widget = forms.CheckboxSelectMultiple,
        required = False
    )
    chemical_treatment = forms.MultipleChoiceField(
        label='Хімічна обробка',
        choices=Item.TREATMENT,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    state = forms.MultipleChoiceField(
        label='Стан',
        choices=Item.STATE,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    seasonality = forms.MultipleChoiceField(
        label='Сезонність',
        choices=Item.SEASONALITY,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    min_price = forms.FloatField(
        label='Мінімальна ціна',
        required=False
    )
    max_price = forms.FloatField(
        label='Максимальна ціна',
        required=False
    )
    date_of_appearance = forms.MultipleChoiceField(
        label='Дата появи товару',
        choices= [(x['date_of_appearance'], x['date_of_appearance']) for x in Item.objects.values('date_of_appearance').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    supplier = forms.MultipleChoiceField(
        label='Постачальник',
        choices=[(x.id_supplier, x.company_name) for x in Supplier.objects.all()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class CustomerFilterForm(forms.Form):
    customer_name = forms.MultipleChoiceField(
        label='Ім\'я',
        choices=[(x['customer_name'], x['customer_name']) for x in
                 Customer.objects.values('customer_name').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    customer_surname = forms.MultipleChoiceField(
        label='Прізвище',
        choices=[(x['customer_surname'], x['customer_surname']) for x in
                 Customer.objects.values('customer_surname').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    customer_middle_name = forms.MultipleChoiceField(
        label='По-батькові',
        choices=[(x['customer_middle_name'], x['customer_middle_name']) for x in
                 Customer.objects.values('customer_middle_name').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    customer_city = forms.MultipleChoiceField(
        label='Місто',
        choices=[(x['customer_city'], x['customer_city']) for x in
                 Customer.objects.values('customer_city').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    customer_address = forms.MultipleChoiceField(
        label='Вулиця',
        choices=[(x['customer_address'], x['customer_address']) for x in
                 Customer.objects.values('customer_address').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    min_number = forms.FloatField(
        label='Мінімальний номер будинку',
        required=False
    )
    max_number = forms.FloatField(
        label='Максимальна номер будинку',
        required=False
    )
    customer_phone_number = forms.MultipleChoiceField(
        label='Телефон',
        choices=[(x['customer_phone_number'], x['customer_phone_number']) for x in
                 Customer.objects.values('customer_phone_number').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    customer_email = forms.MultipleChoiceField(
        label='Пошта',
        choices=[(x['customer_email'], x['customer_email']) for x in
                 Customer.objects.values('customer_email').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    customer_passport_code = forms.MultipleChoiceField(
        label='Код паспорту',
        choices=[(x['customer_passport_code'], x['customer_passport_code']) for x in Customer.objects.values('customer_passport_code').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    customer_date_of_birth = forms.MultipleChoiceField(
        label='День народження',
        choices=[(x['customer_date_of_birth'], x['customer_date_of_birth']) for x in
                 Customer.objects.values('customer_date_of_birth').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    customer_password = forms.MultipleChoiceField(
        label='Пароль',
        choices=[(x['customer_password'], x['customer_password']) for x in
                 Customer.objects.values('customer_password').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    customer_credit_card = forms.MultipleChoiceField(
        label='Номер кредитної карти',
        choices=[(x['customer_credit_card'], x['customer_credit_card']) for x in
                 Customer.objects.values('customer_credit_card').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class ReceiptFilterForm(forms.Form):
    id_item = forms.MultipleChoiceField(
        label='Товар',
        choices=[(x.id_item, x.type) for x in Item.objects.all()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    id_customer = forms.MultipleChoiceField(
        label='Покупець',
        choices=[(x.id_customer, x.customer_name) for x in Customer.objects.all()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    date_of_purchase = forms.MultipleChoiceField(
        label='Дата покупки',
        choices=[(x['date_of_purchase'], x['date_of_purchase']) for x in
                 Receipt.objects.values('date_of_purchase').distinct()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    min_the_item_cost = forms.FloatField(
        label='Мінімальна ціна певного товару',
        required=False
    )
    max_the_item_cost = forms.FloatField(
        label='Максимальна ціна певного товару',
        required=False
    )
    method_of_delivery = forms.MultipleChoiceField(
        label='Тип доставки',
        choices=Receipt.DELIVERY,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    payment_type = forms.MultipleChoiceField(
        label='Тип оплати',
        choices=Receipt.PAYMENT,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class SQLQueryForm(forms.Form):
    sql_query = forms.CharField(initial='SELECT ', widget=forms.Textarea)


class SortByItem(forms.Form):
    is_reversed = forms.BooleanField(label='Зворотній порядок', required=False)
    sort_by = forms.ChoiceField(label='Сортувати за', choices=[
        ("id_item", "ID"),
        ("type", "Тип"),
        ("brand", "Бренд"),
        ("size", "Розмір"),
        ("gender", "Приналежність"),
        ("color", "Колір"),
        ("fabric", "Тканина"),
        ("chemical_treatment", "Хімічна обробка"),
        ("state", "Стан"),
        ("seasonality", "Сезонність"),
        ("price", "Ціна"),
        ("date_of_appearance", "Дата появи"),
        ("supplier", "Постачальник")])


class SortBySupplier(forms.Form):
    is_reversed = forms.BooleanField(label='Зворотній порядок', required=False)
    sort_by = forms.ChoiceField(label='Сортувати за', choices=[
        ("id_supplier", "ID"),
        ("company_name", "Назва компанії"),
        ("contact_person_name", "Ім\'я контактної персони"),
        ("contact_person_surname", "Прізвище контактної персони"),
        ("phone_number", "Телефон"),
        ("city", "Місто"),
        ("email", "Пошта")])


class SortByFabric(forms.Form):
    is_reversed = forms.BooleanField(label='Зворотній порядок', required=False)
    sort_by = forms.ChoiceField(label='Сортувати за', choices=[
        ("id_fabric", "ID"),
        ("fabric_name", "Назва тканини"),
        ("destiny", "Щільність"),
        ("elasticity", "Еластичність"),
        ("breathability", "Повітропроникність"),
        ("surface_texture", "Текстура"),
        ("compression_resistance", "Стійкість до стиснення"),
        ("color_fastness", "Стійкість кольору")])


class SortByCustomer(forms.Form):
    is_reversed = forms.BooleanField(label='Зворотній порядок', required=False)
    sort_by = forms.ChoiceField(label='Сортувати за', choices=[
        ("id_customer", "ID"),
        ("customer_name", "Ім\'я'"),
        ("customer_surname", "Прізвище"),
        ("customer_middle_name", "По-батькові"),
        ("customer_city", "Місто"),
        ("customer_address", "Вулиця"),
        ("customer_number_of_house", "Номер будинку"),
        ("customer_phone_number", "Телефон"),
        ("customer_email", "Пошта"),
        ("customer_passport_code", "Код паспорту"),
        ("customer_date_of_birth", "День народження"),
        ("customer_password", "Пароль"),
        ("customer_credit_card", "Номер кредитної карти")])


class SortByIReceipt(forms.Form):
    is_reversed = forms.BooleanField(label='Зворотній порядок', required=False)
    sort_by = forms.ChoiceField(label='Сортувати за', choices=[
        ("id_receipt", "ID"),
        ("id_item", "Товар"),
        ("id_customer", "Покупець"),
        ("date_of_purchase", "Дата покупки"),
        ("the_item_cost", "Вартість"),
        ("method_of_delivery", "Тип доставки"),
        ("payment_type", "Тип оплати"),
       ])
