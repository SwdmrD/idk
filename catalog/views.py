from django.shortcuts import render
from .models import Item, Size, State

from django.views.generic.edit import UpdateView
from django.views.generic import CreateView
from django.views.generic import DeleteView


def index(request):
    items = Item.objects.all()
    sizes = Size.objects.all()
    states = State.objects.all()
    return render(request, 'catalog/Home.html',
                  {'items': items, 'sizes': sizes, 'states': states})

def search(request):
    items = Item.objects.all()
    sizes = Size.objects.all()
    states = State.objects.all()
    return render(request, 'catalog/search_list.html',{'items': items, 'sizes': sizes, 'states': states})
def result(request):
    size_id = request.GET.get('size')
    state_id = request.GET.get('state')

    items = Item.objects.all()

    if size_id:
        items = items.filter(item_size_id=size_id)

    if state_id:
        items = items.filter(item_state_id=state_id)
    return render(request, 'catalog/result.html', {'items': items})
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

class UpdateItemView(UpdateView):
    model = Item
    template_name = "catalog/editor_item.html"
    fields = "__all__"
    success_url = "/items"

class UpdateSizeView(UpdateView):
    model = Size
    template_name = "catalog/editor_size.html"
    fields = "__all__"
    success_url = "/items"

class UpdateStateView(UpdateView):
    model = State
    template_name = "catalog/editor_state.html"
    fields = "__all__"
    success_url = "/items"

class DeleteItemView(DeleteView):
    model = Item
    template_name = "catalog/delete_item.html"
    success_url = "/items"

class DeleteSizeView(DeleteView):
    model = Size
    template_name = "catalog/delete_size.html"
    success_url = "/items"

class DeleteStateView(DeleteView):
    model = State
    template_name = "catalog/delete_state.html"
    success_url = "/items"