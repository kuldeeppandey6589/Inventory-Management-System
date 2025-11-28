from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, InvoiceLine,buyer
from inventory.models import Stock

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer','is_interstate']
InvoiceLineFormSet = inlineformset_factory(
    Invoice, InvoiceLine,
    fields=('product','qty','unit_price','discount_amount'),
    extra=20, can_delete=True
)
