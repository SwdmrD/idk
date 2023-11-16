from django.shortcuts import render
from datetime import datetime, timedelta
from django.views import View
from .models import Item, Fabric, Supplier, Customer, Receipt
from .forms import ProductFilterForm

from django.views.generic.edit import UpdateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.db import connection
from .forms import SQLQueryForm
from django.db.utils import OperationalError


def index(request):
    items = Item.objects.all()
    fabrics = Fabric.objects.all()
    suppliers = Supplier.objects.all()
    customers = Customer.objects.all()
    receipts = Receipt.objects.all()
    return render(request, 'catalog/Home.html',
                  {'items': items, 'fabrics': fabrics, 'suppliers': suppliers, 'customers': customers, 'receipts': receipts})

def edit_request1(request):
    suppliers = Supplier.objects.all()
    items = Item.objects.all()
    fabrics = Fabric.objects.all()

    return render(request,'catalog/Requests.html', {'items': items, 'fabrics': fabrics, 'suppliers': suppliers})


def edit_request(request):
    result = ''
    error_message = None
    items = Item.objects.all()
    fabrics = Fabric.objects.all()
    suppliers = Supplier.objects.all()
    column_names = []
    if request.method == 'POST':
        form = SQLQueryForm(request.POST)
        if form.is_valid():
            sql_query = form.cleaned_data['sql_query']
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql_query)
                    result = cursor.fetchall()
                    column_names = [col[0] for col in cursor.description]
                except OperationalError as e:
                    error_message = "Нічого не знайдено"
    else:
        form = SQLQueryForm()

    return render(request, 'Catalog/Requests.html',
                  {'items': items, 'fabrics': fabrics, 'suppliers': suppliers, 'form': form,'result': result,
                   'error_message': error_message, 'column_names': column_names})


def filters(request):
    filtered_products = None
    if request.method == 'GET':
        form = ProductFilterForm(request.GET)
        if form.is_valid():
            destiny_values = form.cleaned_data.get('destiny', [])
            elasticity_values = form.cleaned_data.get('elasticity', [])
            breathability_values = form.cleaned_data.get('breathability', [])
            filtered_products = Fabric.objects.filter(
                destiny__in=destiny_values,
                elasticity__in=elasticity_values,
                breathability__in=breathability_values
            )
        return render(request, 'catalog/search_list.html', {'form': form, 'filtered_products': filtered_products})
    else:
        form = ProductFilterForm()
    return render(request, 'catalog/search_list.html', {'form': form})


def result(request):
    if request.method == 'GET':
        form = ProductFilterForm(request.GET)
        if form.is_valid():
            destiny_values = form.cleaned_data.get('destiny', [])
            elasticity_values = form.cleaned_data.get('elasticity', [])
            breathability_values = form.cleaned_data.get('breathability', [])

            # Perform filtering using selected parameters
            filtered_products = Fabric.objects.filter(
                destiny__in=destiny_values,
                elasticity__in=elasticity_values,
                breathability__in=breathability_values
            )

            return render(request, 'catalog/result.html', {'form': form, 'filtered_products': filtered_products})

    else:
        form = ProductFilterForm()

    return render(request, 'catalog/result.html', {'form': form})


def list(request):
    items = Item.objects.all()
    fabrics = Fabric.objects.all()
    suppliers = Supplier.objects.all()
    customers = Customer.objects.all()
    receipts = Receipt.objects.all()
    return render(request, 'catalog/list.html', {'items': items, 'fabrics': fabrics, 'suppliers': suppliers, 'customers': customers, 'receipts': receipts})




class CreateItemView(CreateView): #Речі
    model = Item
    template_name = "catalog/Forms/add_form.html"
    fields = "__all__"
    success_url = "/items" 


class UpdateItemView(UpdateView):
    model = Item
    template_name = "catalog/Forms/editor_form.html"
    fields = "__all__"
    success_url = "/items"


class DeleteItemView(DeleteView):
    model = Item
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/items"


class CreateCustomerView(CreateView): #клієнти
    model = Customer
    template_name = "catalog/Forms/add_form.html"
    fields = "__all__"
    success_url = "/items"


class UpdateCustomerView(UpdateView):
    model = Customer
    template_name = "catalog/Forms/editor_form.html"
    fields = "__all__"
    success_url = "/items"


class DeleteCustomerView(DeleteView):
    model = Customer
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/items"

class CreateFabricView(CreateView): #тканина
    model = Fabric
    template_name = "catalog/Forms/add_form.html"
    fields = "__all__"
    success_url = "/items"


class UpdateFabricView(UpdateView):
    model = Fabric
    template_name = "catalog/Forms/editor_form.html"
    fields = "__all__"
    success_url = "/items"


class DeleteFabricView(DeleteView):
    model = Fabric
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/items"

class CreateSupplierView(CreateView): #постачальник
    model = Supplier
    template_name = "catalog/Forms/add_form.html"
    fields = "__all__"
    success_url = "/items"


class UpdateSupplierView(UpdateView):
    model = Supplier
    template_name = "catalog/Forms/editor_form.html"
    fields = "__all__"
    success_url = "/items"


class DeleteSupplierView(DeleteView):
    model = Supplier
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/items"

class CreateReceiptView(CreateView):  #Чеки
    model = Receipt
    template_name = "catalog/Forms/add_form.html"
    fields = "__all__"
    success_url = "/items"

class UpdateReceiptrView(UpdateView):
    model = Receipt
    template_name = "catalog/Forms/editor_form.html"
    fields = "__all__"
    success_url = "/items"

class DeleteReceiptView(DeleteView):
    model = Receipt
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/items"

