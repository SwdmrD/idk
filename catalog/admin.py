from django.contrib import admin
from .models import Item, Fabric, Supplier, Customer, Receipt

admin.site.register(Item)
admin.site.register(Fabric)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Receipt)
