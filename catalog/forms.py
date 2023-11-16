from .models import Item, Fabric, Supplier, Customer, Receipt
from django import forms
from django.forms import ModelForm


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"


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

class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = "__all__"

class ProductFilterForm(forms.Form):
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


class SQLQueryForm(forms.Form):
    sql_query = forms.CharField(widget=forms.Textarea)
