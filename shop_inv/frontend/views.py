from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.utils.timezone import localdate
from django.db.models import Sum
from catalog.models import Product
from sales.models import Invoice
from inventory.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout as auth_logout

@never_cache
@cache_control(must_revalidate=True, no_cache=True, no_store=True)
def dashboard(request):
    today = localdate()
    today_total = Invoice.objects.filter(date__date=today).aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    ctx={'stats':{'total_products': Product.objects.count(),'total_invoices': Invoice.objects.count(),'today_total': today_total}}
    return render(request, 'dashboard.html', ctx)


@cache_control(must_revalidate=True, no_cache=True, no_store=True)
def index(req): 
    if req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']
        
        if username == 'admin@gmail.com' and password == 'admin123':
                req.session['is_authenticated'] = True
                return redirect('frontend:dashboard')
        else:
            messages.error(req, 'Invalid username or password!')
            return render(req,'index.html')
    return render(req, 'index.html')

@never_cache
@cache_control(no_store=True,no_cache=True,must_revalidate=True)        
def logout(req):
    try:
        del req.session['username']
        return redirect('frontend:index')
    except KeyError:
        pass
    return redirect('frontend:index')

def logout_view(request):
    auth_logout(request)
    return redirect('index')

def stock_move(req):
    stockmove = Stock.objects.all()
    return render(req, 'dashboard.html', {'stockmove': stockmove})