from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path
from .models import Customer, Invoice, InvoiceLine
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=('name','phone','gstin'); search_fields=('name','phone','gstin')
class InvoiceLineInline(admin.TabularInline):
    model=InvoiceLine; extra=1; autocomplete_fields=('product',)
    fields=('product','qty','unit_price','discount_amount')
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines=[InvoiceLineInline]
    list_display=('number','date','customer','subtotal','cgst','sgst','igst','grand_total')
    date_hierarchy='date'; search_fields=('number','customer__name')
    readonly_fields=('subtotal','cgst','sgst','igst','grand_total')
