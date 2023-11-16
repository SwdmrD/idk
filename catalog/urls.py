from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='home'),
    path('edit_request', views.edit_request, name='edit_request'),
    path('items',  views.list, name='lists'),
    path('filtration', views.filters, name='filtration'),
    path('result_filtration', views.result, name='filter_products'),

    path('items/new', views.CreateItemView.as_view(), name='new_lists'),
    path('edit_item/<int:pk>/', views.UpdateItemView.as_view(), name='edit_item'),
    path('delete_item/<int:pk>/', views.DeleteItemView.as_view(), name='delete_item'),

    path('customer/new', views.CreateCustomerView.as_view(), name='new_customer'),
    path('edit_customer/<int:pk>/', views.UpdateCustomerView.as_view(), name='edit_customer'),
    path('delete_customer/<int:pk>/', views.DeleteCustomerView.as_view(), name='delete_customer'),

    path('fabric/new', views.CreateFabricView.as_view(), name='new_fabric'),
    path('edit_fabric/<int:pk>/', views.UpdateFabricView.as_view(), name='edit_fabric'),
    path('delete_fabric/<int:pk>/', views.DeleteFabricView.as_view(), name='delete_fabric'),

    path('supplier/new', views.CreateFabricView.as_view(), name='new_supplier'),
    path('edit_supplier/<int:pk>/', views.UpdateSupplierView.as_view(), name='edit_supplier'),
    path('delete_supplier/<int:pk>/', views.DeleteSupplierView.as_view(), name='delete_supplier'),

    path('receipt/new', views.CreateReceiptView.as_view(), name='new_receipt'),
    path('edit_receipt/<int:pk>/', views.UpdateReceiptrView.as_view(), name='edit_receipt'),
    path('delete_receipt/<int:pk>/', views.DeleteReceiptView.as_view(), name='delete_receipt'),


]
