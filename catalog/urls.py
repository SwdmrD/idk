from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('search_items', views.search, name='search'),
    path('filter_items/', views.result, name='filter_items'),
    path('items', views.list, name='lists'),
    path('items/new', views.CreateItemView.as_view(), name='new_lists'),
    path('size/new', views.CreateSizeView.as_view(), name='new_size'),
    path('state/new', views.CreateStateView.as_view(), name='new_state'),
    path('edit_item/<int:pk>/', views.UpdateItemView.as_view(), name='edit_item'),
    path('edit_size/<int:pk>/', views.UpdateSizeView.as_view(), name='edit_size'),
    path('edit_state/<int:pk>/', views.UpdateStateView.as_view(), name='edit_state'),
    path('delete_item/<int:pk>/', views.DeleteItemView.as_view(), name='delete_item'),
    path('delete_size/<int:pk>/', views.DeleteSizeView.as_view(), name='delete_size'),
    path('delete_state/<int:pk>/', views.DeleteStateView.as_view(), name='delete_state'),


]
