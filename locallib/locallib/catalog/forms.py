from .models import Item
from .models import Size
from django.forms import ModelForm

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
class SizeForm(ModelForm):
    class Meta:
        model = Size
        fields = "__all__"