from django.db import models
from catalog.models import Product
class Stock(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE,related_name='stock')
    quantity_on_hand=models.IntegerField(default=0)
    def __str__(self): return f"{self.product.sku} - {self.quantity_on_hand}"
class StockMovement(models.Model):
    REASONS=[('OPENING','Opening Balance'),('PURCHASE','Purchase In'),('SALE','Sale Out'),('RETURN','Sales Return In'),('ADJUST','Adjustment')]
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)
    qty=models.IntegerField(help_text='+ for in, - for out')
    reason=models.CharField(max_length=10, choices=REASONS)
    reference=models.CharField(max_length=100, blank=True, help_text='Invoice or note no.')
    class Meta: ordering=['-datetime']
    def __str__(self): return f"{self.product.sku} {self.qty} ({self.reason})"
