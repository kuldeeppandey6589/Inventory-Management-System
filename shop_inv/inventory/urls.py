from django.urls import path
from .views import *
from . import views

app_name='inventory'

urlpatterns = [
    path('stockmanage/',views.stockmanage,name='stockmanage'),
    path('view_stock/',views.view_stock,name='view_stock'),
    path('add_stock/',views.add_stock,name='add_stock'),
]

