from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import StockMovement, Stock
@receiver(post_save, sender=StockMovement)
def apply_stock_movement(sender, instance, created, **kwargs):
    if not created: return
    with transaction.atomic():
        stock, _ = Stock.objects.select_for_update().get_or_create(product=instance.product)
        stock.quantity_on_hand = (stock.quantity_on_hand or 0) + instance.qty
        stock.save()

