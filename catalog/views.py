from django.shortcuts import render
from .models import Item, Fabric, Supplier, Customer, Receipt
from .forms import FabricFilterForm, SupplierFilterForm, SupplierForm, ItemForm, ItemFilterForm, ItemForm2, SortByForm
from django.db.models import Q, CharField
from django.db.models.functions import Lower
from django.views.generic.edit import UpdateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.db import connection
from .forms import SQLQueryForm
from django.db.utils import OperationalError


def home(request):
    items = Item.objects.all()
    fabrics = Fabric.objects.all()
    suppliers = Supplier.objects.all()
    customers = Customer.objects.all()
    receipts = Receipt.objects.all()
    return render(request, 'catalog/Home.html',
                  {'items': items, 'fabrics': fabrics, 'suppliers': suppliers, 'customers': customers, 'receipts': receipts})


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

    return render(request, 'catalog/Requests.html',
                  {'items': items, 'fabrics': fabrics, 'suppliers': suppliers, 'form': form,'result': result,
                   'error_message': error_message, 'column_names': column_names})


def filters_fabric(request):
    form = FabricFilterForm(request.GET)
    if request.method == 'GET' and form.is_valid():
        destiny_values = form.cleaned_data.get('destiny')
        elasticity_values = form.cleaned_data.get('elasticity')
        breathability_values = form.cleaned_data.get('breathability')
        surface_texture_values = form.cleaned_data.get('surface_texture')
        compression_resistance_values = form.cleaned_data.get('compression_resistance')
        color_fastness_values = form.cleaned_data.get('color_fastness')
        q_objects = Q()
        if destiny_values:
            q_objects |= Q(destiny__in=destiny_values)
        if elasticity_values:
            q_objects |= Q(elasticity__in=elasticity_values)
        if breathability_values:
            q_objects |= Q(breathability__in=breathability_values)
        if surface_texture_values:
            q_objects |= Q(surface_texture__in=surface_texture_values)
        if compression_resistance_values:
            q_objects |= Q(compression_resistance__in=compression_resistance_values)
        if color_fastness_values:
            q_objects |= Q(color_fastness__in=color_fastness_values)
        filtered_fabrics = Fabric.objects.filter(q_objects)
    else:
        filtered_fabrics = Fabric.objects.all()
        form = FabricFilterForm()
    return render(request, 'catalog/filtration/filtration_fabric.html', {'form': form, 'filtered_fabrics': filtered_fabrics})


def filters_item(request):
    form = ItemFilterForm(request.GET)
    if request.method == 'GET' and form.is_valid():
        brand_values = form.cleaned_data.get('brand')
        size_values = form.cleaned_data.get('size')
        gender_values = form.cleaned_data.get('gender')
        color_values = form.cleaned_data.get('color')
        fabric_values = form.cleaned_data.get('fabric', [])
        chemical_treatment_values = form.cleaned_data.get('chemical_treatment')
        state_values = form.cleaned_data.get('state')
        seasonality_values = form.cleaned_data.get('seasonality')
        price_values = form.cleaned_data.get('price')
        date_of_appearance_values = form.cleaned_data.get('date_of_appearance', [])
        supplier_values = form.cleaned_data.get('supplier', [])

        q_objects = Q()
        if brand_values:
            q_objects |= Q(brand__in=brand_values)
        if size_values:
            q_objects |= Q(size__in=size_values)
        if gender_values:
            q_objects |= Q(gender__in=gender_values)
        if color_values:
            q_objects |= Q(color__in=color_values)
        if fabric_values:
            q_objects |= Q(fabric__in=fabric_values)
        if chemical_treatment_values:
            q_objects |= Q(chemical_treatment__in=chemical_treatment_values)
        if state_values:
            q_objects |= Q(state__in=state_values)
        if seasonality_values:
            q_objects |= Q(seasonality__in=seasonality_values)
        if date_of_appearance_values:
            q_objects |= Q(date_of_appearance__in=date_of_appearance_values)
        if supplier_values:
            q_objects |= Q(supplier__in=supplier_values)

        filtered_items = Item.objects.filter(q_objects)
    else:
        filtered_items = Supplier.objects.all()
        form = ItemFilterForm()
    return render(request, 'catalog/filtration/filtration_item.html', {'form': form, 'filtered_items': filtered_items})


def filters_supplier(request):
    form = SupplierFilterForm(request.GET)
    if request.method == 'GET' and form.is_valid():
        contact_person_name_values = form.cleaned_data.get('contact_person_name', [])
        contact_person_surname_values = form.cleaned_data.get('contact_person_surname', [])
        phone_number_values = form.cleaned_data.get('phone_number', [])
        city_values = form.cleaned_data.get('city', [])
        email_values = form.cleaned_data.get('email', [])
        q_objects = Q()
        if contact_person_name_values:
            q_objects |= Q(contact_person_name__in=contact_person_name_values)
        if contact_person_surname_values:
            q_objects |= Q(contact_person_surname__in=contact_person_surname_values)
        if phone_number_values:
            q_objects |= Q(phone_number__in=phone_number_values)
        if city_values:
            q_objects |= Q(city__in=city_values)
        if email_values:
            q_objects |= Q(email__in=email_values)
        filtered_suppliers = Supplier.objects.filter(q_objects)
    else:
        filtered_suppliers = Supplier.objects.all()
        form = SupplierFilterForm()
    return render(request, 'catalog/filtration/filtration_supplier.html', {'form': form, 'filtered_suppliers': filtered_suppliers})


def list(request):
    items = Item.objects.all()
    fabrics = Fabric.objects.all()
    suppliers = Supplier.objects.all()
    customers = Customer.objects.all()
    receipts = Receipt.objects.all()
    
    form = SortByForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        is_reversed = form.cleaned_data['is_reversed']
        if form.cleaned_data['sort_by'] == 'price':
            items = items.order_by(f'{"-" if is_reversed else "" }price')

    context = {'items': items,
               'fabrics': fabrics,
               'suppliers': suppliers,
               'customers': customers,
               'receipts': receipts,
               'sort_form': form}
    return render(request, 'catalog/list.html', context)


def search_item(request):
    query = request.GET.get('q')
    items = Item.objects.all()
    if request.method == 'GET' and query:
        items = Item.objects.filter(
            Q(type__iregex=query) |
            Q(brand__iregex=query) |
            Q(supplier__company_name__iregex=query) |
            Q(fabric__fabric_name__iregex=query) |
            Q(size__iregex=query) |
            Q(gender__iregex=query) |
            Q(color__iregex=query) |
            Q(chemical_treatment__iregex=query) |
            Q(seasonality__iregex=query) |
            Q(state__iregex=query)
        )
    return render(request, 'catalog/search/search_item.html', {'items': items})


def search_fabric(request):
    query = request.GET.get('q')
    fabrics = Fabric.objects.all()
    if request.method == 'GET' and query:
        fabrics = Fabric.objects.filter(
            Q(fabric_name__iregex=query) |
            Q(destiny__iregex=query) |
            Q(elasticity__iregex=query) |
            Q(breathability__iregex=query) |
            Q(surface_texture__iregex=query) |
            Q(compression_resistance__iregex=query) |
            Q(color_fastness__iregex=query)
        )
    return render(request, 'catalog/search/search_fabric.html', {'fabrics': fabrics})


def search_supplier(request):
    query = request.GET.get('q')
    suppliers = Supplier.objects.all()
    if request.method == 'GET' and query:
        suppliers = Supplier.objects.filter(
            Q(company_name__iregex=query) |
            Q(contact_person_name__iregex=query) |
            Q(contact_person_surname__iregex=query) |
            Q(phone_number__iregex=query) |
            Q(city__iregex=query) |
            Q(email__iregex=query)
        )
    return render(request, 'catalog/search/search_supplier.html', {'suppliers': suppliers})

def statistics(request):
    items = Item.objects.all()
    fabrics = Fabric.objects.all()
    suppliers = Supplier.objects.all()
    customers = Customer.objects.all()
    receipts = Receipt.objects.all()
    return render(request, 'catalog/Statistics.html',
                  {'items': items, 'fabrics': fabrics, 'suppliers': suppliers, 'customers': customers,
                   'receipts': receipts})


class CreateItemView(CreateView):
    model = Item
    template_name = "catalog/Forms/add_form.html"
    form_class = ItemForm
    success_url = "/items"


class UpdateItemView(UpdateView):
    model = Item
    template_name = "catalog/Forms/editor_form.html"
    form_class = ItemForm2
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
    form_class = SupplierForm
    success_url = "/items"


class UpdateSupplierView(UpdateView):
    model = Supplier
    template_name = "catalog/Forms/editor_form.html"
    form_class = SupplierForm
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

