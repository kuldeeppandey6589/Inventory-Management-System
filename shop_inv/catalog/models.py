from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=100, unique=True)
    slug=models.SlugField(max_length=120, unique=True, blank=True)
    def __str__(self): return self.name
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField(max_length=200)
    sku=models.CharField(max_length=100, unique=True)
    barcode=models.CharField(max_length=100, blank=True, null=True)
    hsn=models.CharField(max_length=10, blank=True, help_text='HSN code')
    gst_rate=models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    mrp=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_price=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active=models.BooleanField(default=True)
    def __str__(self): 
        return f"{self.name} ({self.sku})"
