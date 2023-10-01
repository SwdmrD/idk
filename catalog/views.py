from django.shortcuts import render, get_object_or_404
from .models import Item
from .models import Size
from .models import State

from django.views.generic.edit import UpdateView
from django.views.generic import CreateView



def index(request):
    items = Item.objects.all()
    sizes = Size.objects.all()
    states = State.objects.all()
    return render(request, 'catalog/Home.html', {'items': items, 'sizes': sizes, 'states': states})


def auth(request):
    return render(request, 'catalog/Authorization.html')

def list(request):
    items = Item.objects.all()
    sizes = Size.objects.all()
    states = State.objects.all()
    return render(request, 'catalog/list.html', {'items': items, 'sizes': sizes, 'states': states})
class CreateItemView(CreateView):
    model = Item
    fields = "__all__"
    success_url = "/items" 


class CreateSizeView(CreateView):
    model = Size
    fields = "__all__"
    success_url = "/items"

class CreateStateView(CreateView):
    model = State
    fields = "__all__"
    success_url = "/items"

class UpdateStateView(UpdateView):
    model = State
    template_name = "editor.html"
    success_url = "/items"
