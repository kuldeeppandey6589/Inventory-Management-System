from django.urls import path
from .views import ProductList, ProductCreate
from . import views
app_name='catalog'
urlpatterns=[
  path('products/', ProductList.as_view(), name='product_list'),
  path('products/new/', ProductCreate.as_view(), name='product_create'),
]
