import datetime
from datetime import date, timedelta
from django.shortcuts import render
from .models import Item, Fabric, Supplier, Customer, Receipt
from .forms import (FabricFilterForm, SupplierFilterForm, SupplierForm,
                    ItemForm, ItemFilterForm, ItemForm2, SortByItem, SortByCustomer, SortByIReceipt,
                    SortBySupplier, SortByFabric, CustomerForm, ReceiptForm, CustomerForm2,
                    CustomerFilterForm, ReceiptFilterForm, ReceiptForm2)
from django.db.models import Q, Count, Avg, Sum, Max, Min
from django.views.generic.edit import UpdateView
from django.views.generic import CreateView, DeleteView
from django.db import connection
from .forms import SQLQueryForm
from django.db.utils import OperationalError
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from .models import Supplier
from datetime import datetime
import os
os.add_dll_directory(r"C:\\Program Files\\GTK3-Runtime Win64\\bin\\")
from weasyprint import HTML
HTML('https://weasyprint.org/').write_pdf('weasyprint-website.pdf')

def home(request):
    return render(request, 'catalog/Home.html')


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


def filters_customer(request):
    form = CustomerFilterForm(request.GET)
    if request.method == 'GET' and form.is_valid():
        customer_name_values = form.cleaned_data.get('customer_name')
        customer_surname_values = form.cleaned_data.get('customer_surname')
        customer_middle_name_values = form.cleaned_data.get('customer_middle_name')
        customer_city_values = form.cleaned_data.get('customer_city')
        customer_address_values = form.cleaned_data.get('customer_address')
        customer_number_of_house_values = form.cleaned_data.get('customer_number_of_house')
        customer_phone_number_values = form.cleaned_data.get('customer_phone_number')
        customer_email_values = form.cleaned_data.get('customer_email')
        customer_passport_code_values = form.cleaned_data.get('customer_passport_code')
        customer_date_of_birth_values = form.cleaned_data.get('customer_date_of_birth')
        customer_password_values = form.cleaned_data.get('customer_password')
        customer_credit_card_values = form.cleaned_data.get('customer_credit_card')
        q_objects = Q()
        if customer_name_values:
            q_objects &= Q(customer_name__in=customer_name_values)
        if customer_surname_values:
            q_objects &= Q(customer_surname__in=customer_surname_values)
        if customer_middle_name_values:
            q_objects &= Q(customer_middle_name__in=customer_middle_name_values)
        if customer_city_values:
            q_objects &= Q(customer_city__in=customer_city_values)
        if customer_address_values:
            q_objects &= Q(customer_address__in=customer_address_values)
        if customer_number_of_house_values:
            q_objects &= Q(customer_number_of_house__in=customer_number_of_house_values)
        if customer_phone_number_values:
            q_objects &= Q(customer_phone_number__in=customer_phone_number_values)
        if customer_email_values:
            q_objects &= Q(customer_email__in=customer_email_values)
        if customer_passport_code_values:
            q_objects &= Q(customer_passport_code__in=customer_passport_code_values)
        if customer_date_of_birth_values:
            q_objects &= Q(customer_date_of_birth__in=customer_date_of_birth_values)
        if customer_password_values:
            q_objects &= Q(customer_password__in=customer_password_values)
        if customer_credit_card_values:
            q_objects &= Q(customer_credit_card__in=customer_credit_card_values)
        filtered_customers = Customer.objects.filter(q_objects)
    else:
        filtered_customers = Customer.objects.all()
        form = CustomerFilterForm()
    return render(request, 'catalog/filtration/filtration_customer.html',
                  {'form': form, 'filtered_customers': filtered_customers})


def filters_receipt(request):
    form = ReceiptFilterForm(request.GET)
    if request.method == 'GET' and form.is_valid():
        id_item_values = form.cleaned_data.get('id_item')
        id_customer_values = form.cleaned_data.get('id_customer')
        date_of_purchase_values = form.cleaned_data.get('date_of_purchase')
        method_of_delivery_values = form.cleaned_data.get('method_of_delivery')
        payment_type_values = form.cleaned_data.get('payment_type')
        min_price = form.cleaned_data.get('min_the_item_cost')
        max_price = form.cleaned_data.get('max_the_item_cost')
        q_objects = Q()
        if id_item_values:
            q_objects &= Q(id_item__in=id_item_values)
        if id_customer_values:
            q_objects &= Q(id_customer__in=id_customer_values)
        if date_of_purchase_values:
            q_objects &= Q(date_of_purchase__in=date_of_purchase_values)
        if min_price is not None:
            q_objects &= Q(the_item_cost__gte=min_price)
        if max_price is not None:
            q_objects &= Q(the_item_cost__lte=max_price)
        if method_of_delivery_values:
            q_objects &= Q(method_of_delivery__in=method_of_delivery_values)
        if payment_type_values:
            q_objects &= Q(payment_type__in=payment_type_values)
        filtered_receipts = Receipt.objects.filter(q_objects)
    else:
        filtered_receipts = Receipt.objects.all()
        form = ReceiptFilterForm()
    return render(request, 'catalog/filtration/filtration_receipt.html',
                  {'form': form, 'filtered_receipts': filtered_receipts})


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


def list_customer(request):
    customers = Customer.objects.all()
    form = SortByCustomer(request.POST or None)
    if request.method == "POST" and form.is_valid():
        is_reversed = form.cleaned_data['is_reversed']
        if form.cleaned_data['sort_by'] == 'id_customer':
            customers = customers.order_by(f'{"-" if is_reversed else ""}id_customer')
        if form.cleaned_data['sort_by'] == 'customer_name':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_name')
        if form.cleaned_data['sort_by'] == 'customer_surname':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_surname')
        if form.cleaned_data['sort_by'] == 'customer_middle_name':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_middle_name')
        if form.cleaned_data['sort_by'] == 'customer_city':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_city')
        if form.cleaned_data['sort_by'] == 'customer_address':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_address')
        if form.cleaned_data['sort_by'] == 'customer_number_of_house':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_number_of_house')
        if form.cleaned_data['sort_by'] == 'customer_phone_number':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_phone_number')
        if form.cleaned_data['sort_by'] == 'customer_email':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_email')
        if form.cleaned_data['sort_by'] == 'customer_passport_code':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_passport_code')
        if form.cleaned_data['sort_by'] == 'customer_date_of_birth':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_date_of_birth')
        if form.cleaned_data['sort_by'] == 'customer_password':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_password')
        if form.cleaned_data['sort_by'] == 'customer_credit_card':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_credit_card')
    context = {'customers': customers,
               'sort_form': form}
    return render(request, 'catalog/tables/table_customer.html', context)


def list_receipt(request):
    receipts = Receipt.objects.all()
    items = Item.objects.all()
    form = SortByIReceipt(request.POST or None)
    if request.method == "POST" and form.is_valid():
        is_reversed = form.cleaned_data['is_reversed']
        if form.cleaned_data['sort_by'] == 'id_receipt':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}id_receipt')
        if form.cleaned_data['sort_by'] == 'id_item':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}id_item')
        if form.cleaned_data['sort_by'] == 'id_customer':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}id_customer')
        if form.cleaned_data['sort_by'] == 'date_of_purchase':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}date_of_purchase')
        if form.cleaned_data['sort_by'] == 'the_item_cost':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}the_item_cost')
        if form.cleaned_data['sort_by'] == 'method_of_delivery':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}method_of_delivery')
        if form.cleaned_data['sort_by'] == 'payment_type':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}payment_type')
    context = {'receipts': receipts,
               'items': items,
               'sort_form': form}
    return render(request, 'catalog/tables/table_receipt.html', context)


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
            Q(price__iregex=query)
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


def search_customer(request):
    query = request.GET.get('q')
    word = ""
    customers = Customer.objects.all()
    if request.method == 'GET' and query:
        word = query
        customers = Customer.objects.filter(
            Q(customer_name__iregex=query) |
            Q(customer_surname__iregex=query) |
            Q(customer_middle_name__iregex=query) |
            Q(customer_city__iregex=query) |
            Q(customer_address__iregex=query) |
            Q(customer_number_of_house__iregex=query) |
            Q(customer_phone_number__iregex=query) |
            Q(customer_email__iregex=query) |
            Q(customer_passport_code__iregex=query) |
            Q(customer_password__iregex=query) |
            Q(customer_credit_card__iregex=query)
        )
    return render(request, 'catalog/search/search_customer.html', {'customers': customers, 'word': word})


def search_receipt(request):
    query = request.GET.get('q')
    word = ""
    receipts = Receipt.objects.all()
    if request.method == 'GET' and query:
        word = query
        receipts = Receipt.objects.filter(
                Q(id_item__type__iregex=query) |
                Q(id_customer__customer_name__iregex=query) |
                Q(id_customer__customer_surname__iregex=query) |
                Q(the_item_cost__iregex=query) |
                Q(method_of_delivery__iregex=query) |
                Q(payment_type__iregex=query)
            )
    return render(request, 'catalog/search/search_receipt.html', {'receipts': receipts, 'word': word})



def statistics(request):
    # Середня ціна речей кожного бренду
    average_price_per_brand = Item.objects.values('brand').annotate(average_price=Avg('price'))
    # Кількість речей кожного бренду
    count_per_brand = Item.objects.values('brand').annotate(count=Count('id_item'))
    # Кількість речей за кожним постачальником
    count_per_supplier = Item.objects.values('supplier__company_name').annotate(count=Count('id_item'))
    # Середня ціна речей кожного постачальника
    average_price_per_supplier = Item.objects.values('supplier__company_name').annotate(average_price=Avg('price'))
    # Постачальники, у яких найбільше поставок
    most_deliveries = count_per_supplier.aggregate(Max('count'))['count__max']
    most_deliveries_suppliers = count_per_supplier.filter(count=most_deliveries)
    # Постачальники, у яких найменше поставок
    least_deliveries = count_per_supplier.aggregate(Min('count'))['count__min']
    least_deliveries_suppliers = count_per_supplier.filter(count=least_deliveries)
    # Постачальники, у яких найбільше продажів
    suppliers_sales_counts = Supplier.objects.annotate(count=Count('item__receipt'))

    # Знайти найбільшу кількість продажів
    max_sales = suppliers_sales_counts.aggregate(Max('count'))['count__max']

    # Отримати постачальників з найбільшою кількістю продажів
    most_sales_suppliers = suppliers_sales_counts.filter(count=max_sales)

    # сума кожного чека
    receipt_totals = Receipt.objects.values('number_of_receipt').annotate(total=Sum('the_item_cost'))
    # Найбільший чек
    biggest_receipt =receipt_totals.aggregate(Max('total'))['total__max']
    biggest_receipts = receipt_totals.filter(total=biggest_receipt)
    # Найменший чек
    smallest_receipt = receipt_totals.aggregate(Min('total'))['total__min']
    smallest_receipts = receipt_totals.filter(total=smallest_receipt)
  # Середня вартість товарів кожного типу тканини
    average_price_per_fabric_type = Item.objects.values('fabric__fabric_name').annotate(average_price=Avg('price'))

    context = {'average_price_per_brand': average_price_per_brand,
               'count_per_brand': count_per_brand,
               'count_per_supplier': count_per_supplier,
               'average_price_per_supplier': average_price_per_supplier,
               'most_deliveries_suppliers': most_deliveries_suppliers,
               'least_deliveries_suppliers': least_deliveries_suppliers,
               'most_sales_suppliers': most_sales_suppliers,
               'biggest_receipts': biggest_receipts,
               'smallest_receipt': smallest_receipt,
               'smallest_receipts': smallest_receipts,
               'average_price_per_fabric_type': average_price_per_fabric_type,
               'receipt_totals': receipt_totals,

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
    response['Content-Disposition'] = f'attachment; filename="№{supplier.company_name}_document.pdf"'

    return response


def choosing_r(request):
    receipts = Receipt.objects.all()
    receipts = receipts.order_by('number_of_receipt').distinct()
    return render(request, 'catalog/documents/receipt.html', {'receipts': receipts})


def generate_r(request, receipt_id):
    today = (date.today() - timedelta(days = 365)).strftime("%d/%m/%Y")
    last_date = (date.today() + timedelta(days = 365)).strftime("%d/%m/%Y")
    try:
        receipt = Receipt.objects.get(pk= receipt_id)
        customer = receipt.id_customer
        receipts = Receipt.objects.filter(number_of_receipt=receipt.number_of_receipt)
        items = [receipt.id_item for receipt in receipts]
        item_ids = [receipt.id_item.id_item for receipt in receipts]
        item = Item.objects.filter(id_item__in=item_ids)
        total_cost = sum(item.price for item in item)

        total_cost = sum(item.price for item in items)
    except Receipt.DoesNotExist:
        raise Http404("Receipt does not exist")
    template_path = 'catalog/documents/receipt_text.html'
    template = get_template(template_path)
    html_content = template.render({'receipts': receipts, 'today': today, 'items': items, 'last_date': last_date,
                                    'customer': customer, 'receipt': receipt, 'total_cost': total_cost})
    pdf_file = HTML(string=html_content).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="№{receipt.id_receipt}_receipt.pdf"'

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


class CreateCustomerView(CreateView):
    model = Customer
    template_name = "catalog/FormsCustomer/add_form.html"
    form_class = CustomerForm
    success_url = "/customers"


class UpdateCustomerView(UpdateView):
    model = Customer
    template_name = "catalog/FormsCustomer/editor_form.html"
    form_class = CustomerForm2
    success_url = "/customers"


class DeleteCustomerView(DeleteView):
    model = Customer
    template_name = "catalog/FormsCustomer/delete_form.html"
    success_url = "/customers"


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
    form_class = ReceiptForm
    success_url = "/receipts"


class UpdateReceiptView(UpdateView):
    model = Receipt
    template_name = "catalog/FormsReceipt/editor_form.html"
    form_class = ReceiptForm2
    success_url = "/receipts"


class DeleteReceiptView(DeleteView):
    model = Receipt
    template_name = "catalog/FormsReceipt/delete_form.html"
    success_url = "/receipts"


