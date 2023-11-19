from .models import Item, Fabric, Supplier, Customer, Receipt
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from datetime import date, timedelta


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
        return price

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
        return price

    def filter_by_price(data, price_ranges):
        filtered_data = []
        for item in data:
            for price_range in price_ranges:
                min_price, max_price = map(int, price_range.split('-'))
                if min_price <= Item.price <= max_price:
                    filtered_data.append(item)
                    break
        return filtered_data

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
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+380 xx-ххх-хх-хх'}),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = "__all__"


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


price_choices = [
    ('0-400', '0-400'),
    ('400-800', '400-800'),
    ('800-1200', '800-1200'),
    ('1200-1600', '1200-1600'),
    ('2000-2400', '2000-2400'),
    ('2400-2800', '2400-2800'),
    ('2800-3200', '2800-3200'),
    ('3200-3600', '3200-3600'),
    ('3600-4000', '3600-4000'),
    ('4000-4400', '4000-4400'),
    ('4400-4800', '4400-4800'),
    ('4800-5000', '4800-5000')]


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
    price = forms.MultipleChoiceField(
        label='Ціна',
        choices=price_choices,
        widget=forms.CheckboxSelectMultiple,
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


class SQLQueryForm(forms.Form):
    sql_query = forms.CharField(initial='SELECT ', widget=forms.Textarea)
