from django.urls import path
from .views import *
app_name='sales'
urlpatterns=[
  path('invoices/new/', invoice_create, name='invoice_create'),
  path('invoices/<int:pk>/', invoice_detail, name='invoice_detail'),
  path('invoices/', invoice_list, name='invoice_list'),
  path('delinv/<int:pk>/', delinv,name='delinv'),
]
