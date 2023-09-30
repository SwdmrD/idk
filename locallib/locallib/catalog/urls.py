from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('authorization/', views.auth, name='authr'),
    path('items', views.list, name='lists'),
    path('items/new', views.CreateItemView.as_view(), name='new_lists'),
    path('size/new', views.CreateSizeView.as_view(), name='new_size'),
    path('state/new', views.CreateStateView.as_view(), name='new_state'),
    path('edit_state/<int:pk>/', views.UpdateStateView.as_view(), name='edit_state'),

]
