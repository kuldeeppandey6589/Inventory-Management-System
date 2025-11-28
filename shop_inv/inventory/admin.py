from django.contrib import admin
from .models import Stock, StockMovement

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display=('product','quantity_on_hand')
    search_fields=('product__name','product__sku')
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display=('product','qty','reason','datetime','reference')
    list_filter=('reason',)
    search_fields=('product__name','product__sku','reference')
    autocomplete_fields=('product',)
