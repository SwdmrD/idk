from .models import Item
from .models import Size
from .models import State
from django.forms import ModelForm

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
class SizeForm(ModelForm):
    class Meta:
        model = Size
        fields = "__all__"

class StateForm(ModelForm):
    class Meta:
        model = State
        fields = "__all__"