from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.db import transaction
from django.db.models import F
from .forms import StockForm
from django.contrib import messages


def stockmanage(req):
    stock = StockMovement.objects.all()
    return render(req, 'stock/stockmanage.html', {'stock': stock})

def view_stock(req):
    viewstock = Stock.objects.all()
    return render(req,'stock/view_stock.html',{'viewstock':viewstock})

def add_stock(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        qty = int(request.POST.get("quantity_on_hand") or 0)

        if not product_id or qty <= 0:
            messages.error(request, "Select a product and enter a positive quantity.")
            products = Product.objects.all()
            return render(request, "stock/stock_move.html", {"products": products})

        product = get_object_or_404(Product, pk=product_id)

        # Create if missing, else increment existing
        stock, _ = Stock.objects.get_or_create(
            product=product, defaults={"quantity_on_hand": 0}
        )
        Stock.objects.filter(pk=stock.pk).update(
            quantity_on_hand=F("quantity_on_hand") + qty
        )
        stock.refresh_from_db()

        messages.success(request, f"Updated '{product.name}': New Qty = {stock.quantity_on_hand}.")
        return redirect("inventory:view_stock")   # change to your page

    products = Product.objects.all()
    return render(request, "stock/stock_move.html", {"products": products})