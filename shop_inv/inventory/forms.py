from django import forms
from . models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["product", "quantity_on_hand"]

