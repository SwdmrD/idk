from django.contrib import admin
from .models import Item
from .models import Size
from .models import State

admin.site.register(Item)
admin.site.register(Size)
admin.site.register(State)
