import os
from datetime import date, timedelta

from django.contrib import messages
from django.db import connection
from django.db.models import Avg, Count, Max, Min, Q, Subquery, Sum
from django.db.utils import OperationalError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import CreateView, DeleteView
from django.views.generic.edit import UpdateView

from .forms import *
from .models import *
os.add_dll_directory(r"C:\\Program Files\\GTK3-Runtime Win64\\bin\\")
from weasyprint import HTML

HTML("https://weasyprint.org/").write_pdf("weasyprint-website.pdf")


def home(request):
    return render(request, 'catalog/Home.html')


def home_admin(request):
    return render(request, 'catalog/HomeAdmin.html')


def login_cust(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            customer_email = form.cleaned_data['customer_email']
            customer_password = form.cleaned_data['customer_password']
            try:
                user = Customer.objects.get(customer_email=customer_email)
                if user.customer_password == customer_password:
                    pk = user.pk
                    customer = get_object_or_404(Customer, pk=pk)
                    return render(request, 'catalog/users_page/home_customer.html', {'customer': customer})
                else:
                    messages.error(request, 'Невірний email або пароль')
            except Customer.DoesNotExist:
                messages.error(request, 'Невірний email або пароль')

    return render(request, 'catalog/customer_login.html', {'form': form})


def home_client(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'catalog/users_page/home_customer.html', {'customer': customer})


def my_purchases(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    receipt = Receipt.objects.filter(id_customer=pk)
    receipt = receipt.order_by('number_of_receipt')
    return render(request, 'catalog/users_page/my_purchases.html', {'customer': customer, 'receipt': receipt})


def purchase(request, customer_pk, item_pk):
    customer = get_object_or_404(Customer, pk=customer_pk)
    item = get_object_or_404(Item, pk=item_pk)

    if request.method == 'POST':
        form = ReceiptForm3(request.POST)
        if form.is_valid():
            new_receipt = form.save(commit=False)
            new_receipt.id_customer = customer
            new_receipt.id_item = item
            new_receipt.save()
            return redirect('my_purchases', pk=customer.pk)
    else:
        form = ReceiptForm3(initial={'id_customer': customer, 'id_item': item})

    return render(request, 'catalog/users_page/purchase.html', {'form': form, 'customer': customer, 'item': item})


def goods(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    receipt = Receipt.objects.filter(id_customer=pk)
    query = request.GET.get('q')
    words = query.split() if query else []
    receipt_item_ids = Receipt.objects.values('id_item')
    items = Item.objects.exclude(id_item__in=Subquery(receipt_item_ids))
    sort_form = SortByItem(request.POST or None)
    form = ItemFilterForm(request.GET)
    q_objects = Q()
    if words:
        search = Q()
        for word in words:
            search |= (
                    Q(id_item__iregex=word) |
                    Q(type__iregex=word) |
                    Q(brand__iregex=word) |
                    Q(supplier__company_name__iregex=word) |
                    Q(fabric__fabric_name__iregex=word) |
                    Q(size__iregex=word) |
                    Q(gender__iregex=word) |
                    Q(color__iregex=word) |
                    Q(chemical_treatment__iregex=word) |
                    Q(seasonality__iregex=word) |
                    Q(state__iregex=word) |
                    Q(price__iregex=word)

            )
        q_objects |= search
    if form.is_valid():
        brand_values = form.cleaned_data.get('brand', [])
        size_values = form.cleaned_data.get('size', [])
        gender_values = form.cleaned_data.get('gender', [])
        color_values = form.cleaned_data.get('color', [])
        fabric_values = form.cleaned_data.get('fabric', [])
        chemical_treatment_values = form.cleaned_data.get('chemical_treatment', [])
        state_values = form.cleaned_data.get('state', [])
        seasonality_values = form.cleaned_data.get('seasonality', [])
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        supplier_values = form.cleaned_data.get('supplier', [])
        filters = Q()
        if brand_values:
            filters &= Q(brand__in=brand_values)
        if size_values:
            filters &= Q(size__in=size_values)
        if gender_values:
            filters &= Q(gender__in=gender_values)
        if color_values:
            filters &= Q(color__in=color_values)
        if fabric_values:
            filters &= Q(fabric__in=fabric_values)
        if chemical_treatment_values:
            filters &= Q(chemical_treatment__in=chemical_treatment_values)
        if state_values:
            filters &= Q(state__in=state_values)
        if seasonality_values:
            filters &= Q(seasonality__in=seasonality_values)
        if min_price is not None:
            filters &= Q(price__gte=min_price)
        if max_price is not None:
            filters &= Q(price__lte=max_price)
        if supplier_values:
            filters &= Q(supplier__in=supplier_values)
        q_objects &= filters
    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_item':
            items = items.order_by(f'{"-" if is_reversed else ""}id_item')
        if sort_form.cleaned_data['sort_by'] == 'type':
            items = items.order_by(f'{"-" if is_reversed else ""}type')
        if sort_form.cleaned_data['sort_by'] == 'brand':
            items = items.order_by(f'{"-" if is_reversed else ""}brand')
        if sort_form.cleaned_data['sort_by'] == 'size':
            items = items.order_by(f'{"-" if is_reversed else ""}size')
        if sort_form.cleaned_data['sort_by'] == 'gender':
            items = items.order_by(f'{"-" if is_reversed else ""}gender')
        if sort_form.cleaned_data['sort_by'] == 'color':
            items = items.order_by(f'{"-" if is_reversed else ""}color')
        if sort_form.cleaned_data['sort_by'] == 'fabric':
            items = items.order_by(f'{"-" if is_reversed else ""}fabric')
        if sort_form.cleaned_data['sort_by'] == 'chemical_treatment':
            items = items.order_by(f'{"-" if is_reversed else ""}chemical_treatment')
        if sort_form.cleaned_data['sort_by'] == 'state':
            items = items.order_by(f'{"-" if is_reversed else ""}state')
        if sort_form.cleaned_data['sort_by'] == 'seasonality':
            items = items.order_by(f'{"-" if is_reversed else ""}seasonality')
        if sort_form.cleaned_data['sort_by'] == 'price':
            items = items.order_by(f'{"-" if is_reversed else ""}price')
        if sort_form.cleaned_data['sort_by'] == 'supplier':
            items = items.order_by(f'{"-" if is_reversed else ""}supplier')
    items = items.filter(q_objects)
    month = datetime.now().month
    season_discounts = {
        "Зима": ["Літо"],
        "Весна": ["Осінь"],
        "Літо": ["Зима"],
        "Осінь": ["Весна"],
        "Демісезон": ["Демісезон"]
    }
    current_season = "Зима" if month in {12, 1, 2} else \
        "Весна" if month in {3, 4, 5} else \
            "Літо" if month in {6, 7, 8} else \
                "Осінь"
    discount = 0.75
    demi_discount = 0.9
    for item in items:
        if current_season in {"Літо", "Зима"} and item.seasonality == "Демісезон":
            item.discounted_price = item.price * demi_discount
        elif item.seasonality in season_discounts.get(current_season, []):
            item.discounted_price = item.price * discount
        else:
            item.discounted_price = item.price

    context = {'items': items,
               'sort_form': sort_form,
               'customer': customer,
               'receipt': receipt,
               'form': form,
               'words': words}
    return render(request, 'catalog/users_page/goods.html', context)


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
                    cursor.execute(sql_query)  # виконання SQL запиту
                    result = cursor.fetchall()   #витягнути всі строки з результату
                    column_names = [col[0] for col in cursor.description]
                except OperationalError as e:
                    error_message = "Нічого не знайдено"
    else:
        form = SQLQueryForm()

    return render(request, 'catalog/Requests.html',
                  {'items': items, 'fabrics': fabrics, 'suppliers': suppliers, 'form': form, 'result': result,
                   'error_message': error_message, 'column_names': column_names})


def list_item(request):
    query = request.GET.get('q')
    words = query.split() if query else []
    items = Item.objects.all()
    sort_form = SortByItem(request.POST or None)
    form = ItemFilterForm(request.GET)
    q_objects = Q()
    if words:
        search = Q()
        for word in words:
            search |= (
                    Q(id_item__iregex=word) |
                    Q(type__iregex=word) |
                    Q(brand__iregex=word) |
                    Q(supplier__company_name__iregex=word) |
                    Q(fabric__fabric_name__iregex=word) |
                    Q(size__iregex=word) |
                    Q(gender__iregex=word) |
                    Q(color__iregex=word) |
                    Q(chemical_treatment__iregex=word) |
                    Q(seasonality__iregex=word) |
                    Q(state__iregex=word) |
                    Q(price__iregex=word)

            )
        q_objects |= search
    if form.is_valid():
        brand_values = form.cleaned_data.get('brand', [])
        size_values = form.cleaned_data.get('size', [])
        gender_values = form.cleaned_data.get('gender', [])
        color_values = form.cleaned_data.get('color', [])
        fabric_values = form.cleaned_data.get('fabric', [])
        chemical_treatment_values = form.cleaned_data.get('chemical_treatment', [])
        state_values = form.cleaned_data.get('state', [])
        seasonality_values = form.cleaned_data.get('seasonality', [])
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        supplier_values = form.cleaned_data.get('supplier', [])
        filters = Q()
        if brand_values:
            filters &= Q(brand__in=brand_values)
        if size_values:
            filters &= Q(size__in=size_values)
        if gender_values:
            filters &= Q(gender__in=gender_values)
        if color_values:
            filters &= Q(color__in=color_values)
        if fabric_values:
            filters &= Q(fabric__in=fabric_values)
        if chemical_treatment_values:
            filters &= Q(chemical_treatment__in=chemical_treatment_values)
        if state_values:
            filters &= Q(state__in=state_values)
        if seasonality_values:
            filters &= Q(seasonality__in=seasonality_values)
        if min_price is not None:
            filters &= Q(price__gte=min_price)
        if max_price is not None:
            filters &= Q(price__lte=max_price)
        if supplier_values:
            filters &= Q(supplier__in=supplier_values)
        q_objects &= filters
    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_item':
            items = items.order_by(f'{"-" if is_reversed else ""}id_item')
        if sort_form.cleaned_data['sort_by'] == 'type':
            items = items.order_by(f'{"-" if is_reversed else ""}type')
        if sort_form.cleaned_data['sort_by'] == 'brand':
            items = items.order_by(f'{"-" if is_reversed else ""}brand')
        if sort_form.cleaned_data['sort_by'] == 'size':
            items = items.order_by(f'{"-" if is_reversed else ""}size')
        if sort_form.cleaned_data['sort_by'] == 'gender':
            items = items.order_by(f'{"-" if is_reversed else ""}gender')
        if sort_form.cleaned_data['sort_by'] == 'color':
            items = items.order_by(f'{"-" if is_reversed else ""}color')
        if sort_form.cleaned_data['sort_by'] == 'fabric':
            items = items.order_by(f'{"-" if is_reversed else ""}fabric')
        if sort_form.cleaned_data['sort_by'] == 'chemical_treatment':
            items = items.order_by(f'{"-" if is_reversed else ""}chemical_treatment')
        if sort_form.cleaned_data['sort_by'] == 'state':
            items = items.order_by(f'{"-" if is_reversed else ""}state')
        if sort_form.cleaned_data['sort_by'] == 'seasonality':
            items = items.order_by(f'{"-" if is_reversed else ""}seasonality')
        if sort_form.cleaned_data['sort_by'] == 'price':
            items = items.order_by(f'{"-" if is_reversed else ""}price')
        if sort_form.cleaned_data['sort_by'] == 'supplier':
            items = items.order_by(f'{"-" if is_reversed else ""}supplier')
    items = items.filter(q_objects)
    month = datetime.now().month
    season_discounts = {
        "Зима": ["Літо"],
        "Весна": ["Осінь"],
        "Літо": ["Зима"],
        "Осінь": ["Весна"],
        "Демісезон": ["Демісезон"]
    }
    current_season = "Зима" if month in {12, 1, 2} else \
        "Весна" if month in {3, 4, 5} else \
            "Літо" if month in {6, 7, 8} else \
                "Осінь"
    discount = 0.75
    demi_discount = 0.9
    for item in items:
        if current_season in {"Літо", "Зима"} and item.seasonality == "Демісезон":
            item.discounted_price = item.price * demi_discount
        elif item.seasonality in season_discounts.get(current_season, []):
            item.discounted_price = item.price * discount
        else:
            item.discounted_price = item.price
    context = {'items': items,
               'sort_form': sort_form,
               'form': form,
               'words': words}
    return render(request, 'catalog/tables/table_item.html', context)


def list_fabric(request):
    query = request.GET.get('q')
    words = query.split() if query else []
    fabrics = Fabric.objects.all()
    sort_form = SortByFabric(request.POST or None)
    form = FabricFilterForm(request.GET)
    q_objects = Q()

    if words:
        search = Q()
        for word in words:
            search |= (
                    Q(id_fabric__iregex=word) |
                    Q(fabric_name__iregex=word) |
                    Q(destiny__iregex=word) |
                    Q(elasticity__iregex=word) |
                    Q(breathability__iregex=word) |
                    Q(surface_texture__iregex=word) |
                    Q(compression_resistance__iregex=word) |
                    Q(color_fastness__iregex=word)
            )
        q_objects |= search

    if form.is_valid():
        destiny_values = form.cleaned_data.get('destiny')
        elasticity_values = form.cleaned_data.get('elasticity')
        breathability_values = form.cleaned_data.get('breathability')
        surface_texture_values = form.cleaned_data.get('surface_texture')
        compression_resistance_values = form.cleaned_data.get('compression_resistance')
        color_fastness_values = form.cleaned_data.get('color_fastness')

        filterss = Q()

        if destiny_values:
            filterss &= Q(destiny__in=destiny_values)
        if elasticity_values:
            filterss &= Q(elasticity__in=elasticity_values)
        if breathability_values:
            filterss &= Q(breathability__in=breathability_values)
        if surface_texture_values:
            filterss &= Q(surface_texture__in=surface_texture_values)
        if compression_resistance_values:
            filterss &= Q(compression_resistance__in=compression_resistance_values)
        if color_fastness_values:
            filterss &= Q(color_fastness__in=color_fastness_values)

        q_objects &= filterss

    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_fabric':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}id_fabric')
        if sort_form.cleaned_data['sort_by'] == 'fabric_name':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}fabric_name')
        if sort_form.cleaned_data['sort_by'] == 'destiny':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}destiny')
        if sort_form.cleaned_data['sort_by'] == 'elasticity':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}elasticity')
        if sort_form.cleaned_data['sort_by'] == 'breathability':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}breathability')
        if sort_form.cleaned_data['sort_by'] == 'surface_texture':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}surface_texture')
        if sort_form.cleaned_data['sort_by'] == 'compression_resistance':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}compression_resistance')
        if sort_form.cleaned_data['sort_by'] == 'color_fastness':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}color_fastness')
    fabrics = fabrics.filter(q_objects)
    context = {'fabrics': fabrics,
               'sort_form': sort_form,
               'form': form,
               'words': words}
    return render(request, 'catalog/tables/table_fabric.html', context)


def list_supplier(request):
    query = request.GET.get('q')
    words = query.split() if query else []
    suppliers = Supplier.objects.all()
    sort_form = SortBySupplier(request.POST or None)
    form = SupplierFilterForm(request.GET)
    q_objects = Q()
    if words:
        search = Q()
        for word in words:
            search |= (
                    Q(id_supplier__iregex=word) |
                    Q(company_name__iregex=word) |
                    Q(contact_person_name__iregex=word) |
                    Q(contact_person_surname__iregex=word) |
                    Q(phone_number__iregex=word) |
                    Q(city__iregex=word) |
                    Q(email__iregex=word)
            )
        q_objects |= search

    if form.is_valid():
        contact_person_name_values = form.cleaned_data.get('contact_person_name', [])
        contact_person_surname_values = form.cleaned_data.get('contact_person_surname', [])
        phone_number_values = form.cleaned_data.get('phone_number', [])
        city_values = form.cleaned_data.get('city', [])
        email_values = form.cleaned_data.get('email', [])
        filters = Q()
        if contact_person_name_values:
            filters &= Q(contact_person_name__in=contact_person_name_values)
        if contact_person_surname_values:
            filters &= Q(contact_person_surname__in=contact_person_surname_values)
        if phone_number_values:
            filters &= Q(phone_number__in=phone_number_values)
        if city_values:
            filters &= Q(city__in=city_values)
        if email_values:
            filters &= Q(email__in=email_values)
        q_objects &= filters
    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_supplier':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}id_supplier')
        if sort_form.cleaned_data['sort_by'] == 'company_name':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}company_name')
        if sort_form.cleaned_data['sort_by'] == 'contact_person_name':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}contact_person_name')
        if sort_form.cleaned_data['sort_by'] == 'contact_person_surname':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}contact_person_surname')
        if sort_form.cleaned_data['sort_by'] == 'phone_number':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}phone_number')
        if sort_form.cleaned_data['sort_by'] == 'city':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}city')
        if sort_form.cleaned_data['sort_by'] == 'email':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}email')
    suppliers = suppliers.filter(q_objects)
    context = {'suppliers': suppliers,
               'sort_form': sort_form,
               'form': form,
               'words': words}
    return render(request, 'catalog/tables/table_supplier.html', context)


def list_customer(request):
    query = request.GET.get('q')
    words = query.split() if query else []
    customers = Customer.objects.all()
    sort_form = SortByCustomer(request.POST or None)
    form = CustomerFilterForm(request.GET)
    q_objects = Q()
    if words:
        search = Q()
        for word in words:
            search |= (
                    Q(id_customer__iregex=word) |
                    Q(customer_name__iregex=word) |
                    Q(customer_surname__iregex=word) |
                    Q(customer_middle_name__iregex=word) |
                    Q(customer_city__iregex=word) |
                    Q(customer_address__iregex=word) |
                    Q(customer_number_of_house__iregex=word) |
                    Q(customer_phone_number__iregex=word) |
                    Q(customer_email__iregex=word) |
                    Q(customer_passport_code__iregex=word) |
                    Q(customer_password__iregex=word) |
                    Q(customer_credit_card__iregex=word)
            )
        q_objects |= search
    if form.is_valid():
        customer_name_values = form.cleaned_data.get('customer_name', [])
        customer_surname_values = form.cleaned_data.get('customer_surname', [])
        customer_middle_name_values = form.cleaned_data.get('customer_middle_name', [])
        customer_city_values = form.cleaned_data.get('customer_city', [])
        customer_address_values = form.cleaned_data.get('customer_address', [])
        customer_number_of_house_values = form.cleaned_data.get('customer_number_of_house', [])
        customer_phone_number_values = form.cleaned_data.get('customer_phone_number', [])
        customer_email_values = form.cleaned_data.get('customer_email', [])
        customer_passport_code_values = form.cleaned_data.get('customer_passport_code', [])
        customer_date_of_birth_values = form.cleaned_data.get('customer_date_of_birth', [])
        customer_password_values = form.cleaned_data.get('customer_password', [])
        customer_credit_card_values = form.cleaned_data.get('customer_credit_card', [])
        filters = Q()
        if customer_name_values:
            filters &= Q(customer_name__in=customer_name_values)
        if customer_surname_values:
            filters &= Q(customer_surname__in=customer_surname_values)
        if customer_middle_name_values:
            filters &= Q(customer_middle_name__in=customer_middle_name_values)
        if customer_city_values:
            filters &= Q(customer_city__in=customer_city_values)
        if customer_address_values:
            filters &= Q(customer_address__in=customer_address_values)
        if customer_number_of_house_values:
            filters &= Q(customer_number_of_house__in=customer_number_of_house_values)
        if customer_phone_number_values:
            filters &= Q(customer_phone_number__in=customer_phone_number_values)
        if customer_email_values:
            filters &= Q(customer_email__in=customer_email_values)
        if customer_passport_code_values:
            filters &= Q(customer_passport_code__in=customer_passport_code_values)
        if customer_date_of_birth_values:
            filters &= Q(customer_date_of_birth__in=customer_date_of_birth_values)
        if customer_password_values:
            filters &= Q(customer_password__in=customer_password_values)
        if customer_credit_card_values:
            filters &= Q(customer_credit_card__in=customer_credit_card_values)
        q_objects &= filters
    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_customer':
            customers = customers.order_by(f'{"-" if is_reversed else ""}id_customer')
        if sort_form.cleaned_data['sort_by'] == 'customer_name':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_name')
        if sort_form.cleaned_data['sort_by'] == 'customer_surname':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_surname')
        if sort_form.cleaned_data['sort_by'] == 'customer_middle_name':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_middle_name')
        if sort_form.cleaned_data['sort_by'] == 'customer_city':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_city')
        if sort_form.cleaned_data['sort_by'] == 'customer_address':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_address')
        if sort_form.cleaned_data['sort_by'] == 'customer_number_of_house':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_number_of_house')
        if sort_form.cleaned_data['sort_by'] == 'customer_phone_number':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_phone_number')
        if sort_form.cleaned_data['sort_by'] == 'customer_email':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_email')
        if sort_form.cleaned_data['sort_by'] == 'customer_passport_code':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_passport_code')
        if sort_form.cleaned_data['sort_by'] == 'customer_date_of_birth':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_date_of_birth')
        if sort_form.cleaned_data['sort_by'] == 'customer_password':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_password')
        if sort_form.cleaned_data['sort_by'] == 'customer_credit_card':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_credit_card')
    customers = customers.filter(q_objects)
    context = {'customers': customers,
               'sort_form': sort_form,
               'form': form,
               'words': words}
    return render(request, 'catalog/tables/table_customer.html', context)


def list_receipt(request):
    query = request.GET.get('q')
    words = query.split() if query else []
    receipts = Receipt.objects.all()
    sort_form = SortByReceipt(request.POST or None)
    form = ReceiptFilterForm(request.GET)
    q_objects = Q()
    if words:
        search = Q()
        for word in words:
            search |= (
                    Q(id_item__type__iregex=word) |
                    Q(id_customer__customer_name__iregex=word) |
                    Q(id_customer__customer_surname__iregex=word) |
                    Q(the_item_cost__iregex=word) |
                    Q(method_of_delivery__iregex=word) |
                    Q(payment_type__iregex=word)
            )
        q_objects |= search

    if form.is_valid():
        id_item_values = form.cleaned_data.get('id_item', [])
        id_customer_values = form.cleaned_data.get('id_customer', [])
        date_of_purchase_values = form.cleaned_data.get('date_of_purchase', [])
        method_of_delivery_values = form.cleaned_data.get('method_of_delivery', [])
        payment_type_values = form.cleaned_data.get('payment_type', [])
        min_price = form.cleaned_data.get('min_the_item_cost')
        max_price = form.cleaned_data.get('max_the_item_cost')
        filters = Q()
        if id_item_values:
            filters &= Q(id_item__in=id_item_values)
        if id_customer_values:
            filters &= Q(id_customer__in=id_customer_values)
        if date_of_purchase_values:
            filters &= Q(date_of_purchase__in=date_of_purchase_values)
        if min_price is not None:
            filters &= Q(the_item_cost__gte=min_price)
        if max_price is not None:
            filters &= Q(the_item_cost__lte=max_price)
        if method_of_delivery_values:
            filters &= Q(method_of_delivery__in=method_of_delivery_values)
        if payment_type_values:
            filters &= Q(payment_type__in=payment_type_values)
        q_objects &= filters
    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_receipt':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}id_receipt')
        if sort_form.cleaned_data['sort_by'] == 'id_item':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}id_item')
        if sort_form.cleaned_data['sort_by'] == 'id_customer':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}id_customer')
        if sort_form.cleaned_data['sort_by'] == 'number_of_receipt':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}number_of_receipt')
        if sort_form.cleaned_data['sort_by'] == 'date_of_purchase':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}date_of_purchase')
        if sort_form.cleaned_data['sort_by'] == 'the_item_cost':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}the_item_cost')
        if sort_form.cleaned_data['sort_by'] == 'method_of_delivery':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}method_of_delivery')
        if sort_form.cleaned_data['sort_by'] == 'payment_type':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}payment_type')
    receipts = receipts.filter(q_objects)
    context = {'receipts': receipts,
               'sort_form': sort_form,
               'form': form,
               'words': words}
    return render(request, 'catalog/tables/table_receipt.html', context)


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
    # сума кожного чека
    start_of_last_week = datetime.now() - timedelta(days=datetime.now().weekday() + 7)
    end_of_last_week = start_of_last_week + timedelta(days=6)
    receipt_totals = Receipt.objects.filter(date_of_purchase__range=[start_of_last_week, end_of_last_week]).values(
        'number_of_receipt').annotate(total=Sum('the_item_cost'))
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
    today = (date.today() - timedelta(days=365)).strftime("%d/%m/%Y")
    last_date = (date.today() + timedelta(days=365)).strftime("%d/%m/%Y")
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
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
    unique_receipt_numbers = Receipt.objects.order_by('number_of_receipt').values_list('number_of_receipt',
                                                                                       flat=True).distinct()
    receipts = []
    for receipt_number in unique_receipt_numbers:
        receipt = Receipt.objects.filter(number_of_receipt=receipt_number).first()
        receipts.append(receipt)

    return render(request, 'catalog/documents/receipt.html', {'receipts': receipts, 'receipt': receipt})


def generate_r(request, receipt_id):
    today = (date.today() - timedelta(days=365)).strftime("%d/%m/%Y")
    last_date = (date.today() + timedelta(days=365)).strftime("%d/%m/%Y")
    try:
        receipt = Receipt.objects.get(pk=receipt_id)
        customer = receipt.id_customer
        receipts = Receipt.objects.filter(number_of_receipt=receipt.number_of_receipt)
        items = [receipt.id_item for receipt in receipts]
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


class CreateCustomerView(CreateView):
    model = Customer
    template_name = "catalog/Forms/add_form.html"
    form_class = CustomerForm
    success_url = "/customers"


class CreateCustomer2View(CreateView):
    model = Customer
    template_name = "catalog/Forms/add_account.html"
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('home_client', args=[str(self.object.pk)])


class UpdateCustomerView(UpdateView):
    model = Customer
    template_name = "catalog/Forms/editor_form.html"
    form_class = CustomerForm2
    success_url = "/customers"


class UpdateCustomer2View(UpdateView):
    model = Customer
    template_name = "catalog/users_page/edit_info.html"
    form_class = CustomerForm2

    def get_success_url(self):
        return reverse('home_client', args=[str(self.object.pk)])


class DeleteCustomerView(DeleteView):
    model = Customer
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/customers"


class CreateFabricView(CreateView):  # тканина
    model = Fabric
    template_name = "catalog/Forms/add_form.html"
    fields = "__all__"
    success_url = "/fabrics"


class UpdateFabricView(UpdateView):
    model = Fabric
    template_name = "catalog/Forms/editor_form.html"
    fields = "__all__"
    success_url = "/fabrics"


class DeleteFabricView(DeleteView):
    model = Fabric
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/fabrics"


class CreateSupplierView(CreateView):  # постачальник
    model = Supplier
    template_name = "catalog/Forms/add_form.html"
    form_class = SupplierForm
    success_url = "/suppliers"


class UpdateSupplierView(UpdateView):
    model = Supplier
    template_name = "catalog/Forms/editor_form.html"
    form_class = SupplierForm
    success_url = "/suppliers"


class DeleteSupplierView(DeleteView):
    model = Supplier
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/suppliers"


class CreateReceiptView(CreateView):  # Чеки
    model = Receipt
    template_name = "catalog/Forms/add_form.html"
    form_class = ReceiptForm
    success_url = "/receipts"


class UpdateReceiptView(UpdateView):
    model = Receipt
    template_name = "catalog/Forms/editor_form.html"
    form_class = ReceiptForm2
    success_url = "/receipts"


class DeleteReceiptView(DeleteView):
    model = Receipt
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/receipts"
