from django.shortcuts import render
from .models import Item
from .models import Size

from django.views.generic import CreateView



def index(request):
    return render(request, 'catalog/Home.html')


def auth(request):
    return render(request, 'catalog/Authorization.html')

def list(request):
    items = Item.objects.all()
    sizes = Size.objects.all()
    return render(request, 'catalog/list.html', {'items': items, 'sizes': sizes})
class CreateItemView(CreateView):
    model = Item
    fields = "__all__"
    success_url = "/items" 

class CreateSizeView(CreateView):
    model = Size
    fields = "__all__"
    success_url = "/items"
