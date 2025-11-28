from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Product

class ProductList(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'
    
class ProductCreate(CreateView):
    model = Product
    fields = ['category','name','sku','barcode','hsn','gst_rate','mrp','selling_price','purchase_price','is_active']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

