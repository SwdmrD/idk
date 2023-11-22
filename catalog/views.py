import datetime
from datetime import date, timedelta
from django.shortcuts import render
from .models import Item, Fabric, Supplier, Customer, Receipt
from .forms import (FabricFilterForm, SupplierFilterForm, SupplierForm,
                    ItemForm, ItemFilterForm, ItemForm2, SortByItem,
                    SortBySupplier, SortByFabric)
from django.db.models import Q, Count, Avg, Sum
from django.views.generic.edit import UpdateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.db import connection
from .forms import SQLQueryForm
from django.db.utils import OperationalError
from django.http import FileResponse
from reportlab.lib.pagesizes import letter, landscape
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from weasyprint import HTML
from .models import Supplier
from reportlab.pdfgen import canvas
import os
os.add_dll_directory(r"C:\\Program Files\\GTK3-Runtime Win64\\bin\\")
from weasyprint import HTML
HTML('https://weasyprint.org/').write_pdf('weasyprint-website.pdf')

def home(request):
    items = Item.objects.all()
    fabrics = Fabric.objects.all()
    suppliers = Supplier.objects.all()
    customers = Customer.objects.all()
    receipts = Receipt.objects.all()
    return render(request, 'catalog/Home.html',
                  {'items': items, 'fabrics': fabrics, 'suppliers': suppliers, 'customers': customers,
                   'receipts': receipts})


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
                  {'items': items, 'fabrics': fabrics, 'suppliers': suppliers, 'form': form, 'result': result,
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
            q_objects &= Q(destiny__in=destiny_values)
        if elasticity_values:
            q_objects &= Q(elasticity__in=elasticity_values)
        if breathability_values:
            q_objects &= Q(breathability__in=breathability_values)
        if surface_texture_values:
            q_objects &= Q(surface_texture__in=surface_texture_values)
        if compression_resistance_values:
            q_objects &= Q(compression_resistance__in=compression_resistance_values)
        if color_fastness_values:
            q_objects &= Q(color_fastness__in=color_fastness_values)
        filtered_fabrics = Fabric.objects.filter(q_objects)
    else:
        filtered_fabrics = Fabric.objects.all()
        form = FabricFilterForm()
    return render(request, 'catalog/filtration/filtration_fabric.html',
                  {'form': form, 'filtered_fabrics': filtered_fabrics})


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
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        date_of_appearance_values = form.cleaned_data.get('date_of_appearance', [])
        supplier_values = form.cleaned_data.get('supplier', [])
        q_objects = Q()
        if brand_values:
            q_objects &= Q(brand__in=brand_values)
        if size_values:
            q_objects &= Q(size__in=size_values)
        if gender_values:
            q_objects &= Q(gender__in=gender_values)
        if color_values:
            q_objects &= Q(color__in=color_values)
        if fabric_values:
            q_objects &= Q(fabric__in=fabric_values)
        if chemical_treatment_values:
            q_objects &= Q(chemical_treatment__in=chemical_treatment_values)
        if state_values:
            q_objects &= Q(state__in=state_values)
        if seasonality_values:
            q_objects &= Q(seasonality__in=seasonality_values)
        if min_price is not None:
            q_objects &= Q(price__gte=min_price)
        if max_price is not None:
            q_objects &= Q(price__lte=max_price)
        if date_of_appearance_values:
            q_objects &= Q(date_of_appearance__in=date_of_appearance_values)
        if supplier_values:
            q_objects &= Q(supplier__in=supplier_values)
        filtered_items = Item.objects.filter(q_objects)
    else:
        filtered_items = Item.objects.all()
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
            q_objects &= Q(contact_person_name__in=contact_person_name_values)
        if contact_person_surname_values:
            q_objects &= Q(contact_person_surname__in=contact_person_surname_values)
        if phone_number_values:
            q_objects &= Q(phone_number__in=phone_number_values)
        if city_values:
            q_objects &= Q(city__in=city_values)
        if email_values:
            q_objects &= Q(email__in=email_values)
        filtered_suppliers = Supplier.objects.filter(q_objects)
    else:
        filtered_suppliers = Supplier.objects.all()
        form = SupplierFilterForm()
    return render(request, 'catalog/filtration/filtration_supplier.html',
                  {'form': form, 'filtered_suppliers': filtered_suppliers})


def list_item(request):
    items = Item.objects.all()
    form = SortByItem(request.POST or None)
    if request.method == "POST" and form.is_valid():
        is_reversed = form.cleaned_data['is_reversed']
        if form.cleaned_data['sort_by'] == 'id_item':
            items = items.order_by(f'{"-" if is_reversed else ""}id_item')
        if form.cleaned_data['sort_by'] == 'type':
            items = items.order_by(f'{"-" if is_reversed else ""}type')
        if form.cleaned_data['sort_by'] == 'brand':
            items = items.order_by(f'{"-" if is_reversed else ""}brand')
        if form.cleaned_data['sort_by'] == 'size':
            items = items.order_by(f'{"-" if is_reversed else ""}size')
        if form.cleaned_data['sort_by'] == 'gender':
            items = items.order_by(f'{"-" if is_reversed else ""}gender')
        if form.cleaned_data['sort_by'] == 'color':
            items = items.order_by(f'{"-" if is_reversed else ""}color')
        if form.cleaned_data['sort_by'] == 'fabric':
            items = items.order_by(f'{"-" if is_reversed else ""}fabric')
        if form.cleaned_data['sort_by'] == 'chemical_treatment':
            items = items.order_by(f'{"-" if is_reversed else ""}chemical_treatment')
        if form.cleaned_data['sort_by'] == 'state':
            items = items.order_by(f'{"-" if is_reversed else ""}state')
        if form.cleaned_data['sort_by'] == 'seasonality':
            items = items.order_by(f'{"-" if is_reversed else ""}seasonality')
        if form.cleaned_data['sort_by'] == 'price':
            items = items.order_by(f'{"-" if is_reversed else ""}price')
        if form.cleaned_data['sort_by'] == 'date_of_appearance':
            items = items.order_by(f'{"-" if is_reversed else ""}date_of_appearance')
        if form.cleaned_data['sort_by'] == 'supplier':
            items = items.order_by(f'{"-" if is_reversed else ""}supplier')
    context = {'items': items,
               'sort_form': form}
    return render(request, 'catalog/tables/table_item.html', context)


def list_fabric(request):
    fabrics = Fabric.objects.all()
    form = SortByFabric(request.POST or None)
    if request.method == "POST" and form.is_valid():
        is_reversed = form.cleaned_data['is_reversed']
        if form.cleaned_data['sort_by'] == 'id_fabric':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}id_fabric')
        if form.cleaned_data['sort_by'] == 'fabric_name':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}fabric_name')
        if form.cleaned_data['sort_by'] == 'destiny':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}destiny')
        if form.cleaned_data['sort_by'] == 'elasticity':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}elasticity')
        if form.cleaned_data['sort_by'] == 'breathability':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}breathability')
        if form.cleaned_data['sort_by'] == 'surface_texture':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}surface_texture')
        if form.cleaned_data['sort_by'] == 'compression_resistance':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}compression_resistance')
        if form.cleaned_data['sort_by'] == 'color_fastness':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}color_fastness')
    context = {'fabrics': fabrics,
               'sort_form': form}
    return render(request, 'catalog/tables/table_fabric.html', context)


def list_supplier(request):
    suppliers = Supplier.objects.all()
    form = SortBySupplier(request.POST or None)
    if request.method == "POST" and form.is_valid():
        is_reversed = form.cleaned_data['is_reversed']
        if form.cleaned_data['sort_by'] == 'id_supplier':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}id_supplier')
        if form.cleaned_data['sort_by'] == 'company_name':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}company_name')
        if form.cleaned_data['sort_by'] == 'contact_person_name':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}contact_person_name')
        if form.cleaned_data['sort_by'] == 'contact_person_surname':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}contact_person_surname')
        if form.cleaned_data['sort_by'] == 'phone_number':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}phone_number')
        if form.cleaned_data['sort_by'] == 'city':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}city')
        if form.cleaned_data['sort_by'] == 'email':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}email')
    context = {'suppliers': suppliers,
               'sort_form': form}
    return render(request, 'catalog/tables/table_supplier.html', context)


def search_item(request):
    query = request.GET.get('q')
    word = ""
    items = Item.objects.all()
    if request.method == 'GET' and query:
        word = query
        items = Item.objects.filter(
            Q(id_item__iregex=query) |
            Q(type__iregex=query) |
            Q(brand__iregex=query) |
            Q(supplier__company_name__iregex=query) |
            Q(fabric__fabric_name__iregex=query) |
            Q(size__iregex=query) |
            Q(gender__iregex=query) |
            Q(color__iregex=query) |
            Q(chemical_treatment__iregex=query) |
            Q(seasonality__iregex=query) |
            Q(state__iregex=query) |
            Q(price__iregex=query) |
            Q(date_of_appearance__iregex=query)
        )
    return render(request, 'catalog/search/search_item.html', {'items': items, 'word':word})


def search_fabric(request):
    query = request.GET.get('q')
    word = ""
    fabrics = Fabric.objects.all()
    if request.method == 'GET' and query:
        word = query
        fabrics = Fabric.objects.filter(
            Q(fabric_name__iregex=query) |
            Q(destiny__iregex=query) |
            Q(elasticity__iregex=query) |
            Q(breathability__iregex=query) |
            Q(surface_texture__iregex=query) |
            Q(compression_resistance__iregex=query) |
            Q(color_fastness__iregex=query)
        )
    return render(request, 'catalog/search/search_fabric.html', {'fabrics': fabrics, 'word': word})


def search_supplier(request):
    query = request.GET.get('q')
    word = ""
    suppliers = Supplier.objects.all()
    if request.method == 'GET' and query:
        word = query
        suppliers = Supplier.objects.filter(
            Q(company_name__iregex=query) |
            Q(contact_person_name__iregex=query) |
            Q(contact_person_surname__iregex=query) |
            Q(phone_number__iregex=query) |
            Q(city__iregex=query) |
            Q(email__iregex=query)
        )
    return render(request, 'catalog/search/search_supplier.html', {'suppliers': suppliers, 'word':word})


def statistics(request):
    size_dict = dict(Item.SIZE)

    average_price = Item.objects.aggregate(average_price=Avg('price'))
    total_price = Item.objects.aggregate(total_price=Sum('price'))
    count_all = Item.objects.aggregate(count_all=Count('id_item'))

    total_suppliers = Supplier.objects.count()
    count_per_supplier = Item.objects.values('supplier__company_name').annotate(count=Count('id_item'))
    average_price_per_supplier = Item.objects.values('supplier__company_name').annotate(count=Avg('price'))
    total_price_per_supplier = Item.objects.values('supplier__company_name').annotate(count=Sum('price'))

    total_fabrics = Fabric.objects.count()
    count_per_destiny = Fabric.objects.values('destiny').annotate(count=Count('id_fabric'))
    count_per_elasticity = Fabric.objects.values('elasticity').annotate(count=Count('id_fabric'))
    count_per_breathability = Fabric.objects.values('breathability').annotate(count=Count('id_fabric'))
    count_per_surface_texture = Fabric.objects.values('surface_texture').annotate(count=Count('id_fabric'))
    count_per_compression_resistance = Fabric.objects.values('compression_resistance').annotate(count=Count('id_fabric'))
    count_per_color_fastness = Fabric.objects.values('color_fastness').annotate(count=Count('id_fabric'))

    average_price_per_brand = Item.objects.values('brand').annotate(average_price=Avg('price'))
    count_per_brand = Item.objects.values('brand').annotate(count=Count('id_item'))
    count_per_size = Item.objects.values('size').annotate(count=Count('id_item'))
    count_per_color = Item.objects.values('color').annotate(count=Count('id_item'))
    count_per_gender = Item.objects.values('gender').annotate(count=Count('id_item'))
    count_per_seasonality = Item.objects.values('seasonality').annotate(count=Count('id_item'))
    count_per_state = Item.objects.values('state').annotate(count=Count('id_item'))
    count_per_chemical_treatment = Item.objects.values('chemical_treatment').annotate(count=Count('id_item'))
    for item in count_per_size:
        item['size'] = size_dict[item['size']]
    context = {'average_price_per_brand': average_price_per_brand,
               'count_per_brand': count_per_brand,
               'count_per_size': count_per_size,
               'count_per_color': count_per_color,
               'count_per_gender': count_per_gender,
               'count_per_seasonality': count_per_seasonality,
               'count_per_state': count_per_state,
               'count_per_chemical_treatment': count_per_chemical_treatment,
               'average_price': average_price['average_price'],
               'total_price': total_price['total_price'],
               'count_all': count_all['count_all'],
               'total_suppliers': total_suppliers,
               'count_per_supplier': count_per_supplier,
               'average_price_per_supplier': average_price_per_supplier,
               'total_price_per_supplier': total_price_per_supplier,
               'count_per_destiny':count_per_destiny,
               'count_per_elasticity': count_per_elasticity,
               'count_per_breathability': count_per_breathability,
               'count_per_surface_texture': count_per_surface_texture,
               'count_per_compression_resistance': count_per_compression_resistance,
               'count_per_color_fastness': count_per_color_fastness,
               'total_fabrics': total_fabrics,
               }
    return render(request, 'catalog/Statistics.html', context)


def choosing(request):
    suppliers = Supplier.objects.all()
    return render(request, 'catalog/documents/agreement.html', {'suppliers': suppliers})


def generate_pdf(request, supplier_id):
    today = (date.today() - timedelta(days = 365)).strftime("%d/%m/%Y")
    last_date = (date.today() + timedelta(days = 365)).strftime("%d/%m/%Y")
    try:
        supplier = Supplier.objects.get(pk= supplier_id)
    except Supplier.DoesNotExist:
        raise Http404("Supplier does not exist")
    template_path = 'catalog/documents/agreement_template.html'
    template = get_template(template_path)
    html_content = template.render({'supplier': supplier, 'today': today, 'last_date': last_date})
    pdf_file = HTML(string=html_content).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{supplier.company_name}_document.pdf"'

    return response


class CreateItemView(CreateView):
    model = Item
    template_name = "catalog/FormsItem/add_form.html"
    form_class = ItemForm
    success_url = "/items"


class UpdateItemView(UpdateView):
    model = Item
    template_name = "catalog/FormsItem/editor_form.html"
    form_class = ItemForm2
    success_url = "/items"


class DeleteItemView(DeleteView):
    model = Item
    template_name = "catalog/FormsItem/delete_form.html"
    success_url = "/items"


class CreateCustomerView(CreateView):  # клієнти
    model = Customer
    template_name = "catalog/FormsCustomer/add_form.html"
    fields = "__all__"
    success_url = "/none"


class UpdateCustomerView(UpdateView):
    model = Customer
    template_name = "catalog/FormsCustomer/editor_form.html"
    fields = "__all__"
    success_url = "/none"


class DeleteCustomerView(DeleteView):
    model = Customer
    template_name = "catalog/FormsCustomer/delete_form.html"
    success_url = "/none"


class CreateFabricView(CreateView):  # тканина
    model = Fabric
    template_name = "catalog/FormsFabric/add_form.html"
    fields = "__all__"
    success_url = "/fabrics"


class UpdateFabricView(UpdateView):
    model = Fabric
    template_name = "catalog/FormsFabric/editor_form.html"
    fields = "__all__"
    success_url = "/fabrics"


class DeleteFabricView(DeleteView):
    model = Fabric
    template_name = "catalog/FormsFabric/delete_form.html"
    success_url = "/fabrics"


class CreateSupplierView(CreateView):  # постачальник
    model = Supplier
    template_name = "catalog/FormsSupplier/add_form.html"
    form_class = SupplierForm
    success_url = "/suppliers"


class UpdateSupplierView(UpdateView):
    model = Supplier
    template_name = "catalog/FormsSupplier/editor_form.html"
    form_class = SupplierForm
    success_url = "/suppliers"


class DeleteSupplierView(DeleteView):
    model = Supplier
    template_name = "catalog/FormsSupplier/delete_form.html"
    success_url = "/suppliers"


class CreateReceiptView(CreateView):  # Чеки
    model = Receipt
    template_name = "catalog/FormsReceipt/add_form.html"
    fields = "__all__"
    success_url = "/none"


class UpdateReceiptrView(UpdateView):
    model = Receipt
    template_name = "catalog/FormsReceipt/editor_form.html"
    fields = "__all__"
    success_url = "/none"


class DeleteReceiptView(DeleteView):
    model = Receipt
    template_name = "catalog/FormsReceipt/delete_form.html"
    success_url = "/none"


