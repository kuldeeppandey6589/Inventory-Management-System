from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.core.paginator import Paginator
from .models import Invoice
from .forms import InvoiceForm, InvoiceLineFormSet
def invoice_list(request):
    invoices = Invoice.objects.order_by('-date')
    page = Paginator(invoices, 20).get_page(request.GET.get('page'))
    return render(request, 'sales/invoice_list.html', {'page': page})
def invoice_detail(request, pk):
    inv = get_object_or_404(Invoice, pk=pk)
    return render(request, 'sales/invoice_detail.html', {'invoice': inv})
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceLineFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                invoice = form.save()
                formset.instance = invoice
                formset.save()
                invoice.post()
            return redirect('sales:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
        formset = InvoiceLineFormSet()
    return render(request, 'sales/invoice_form.html', {'form': form, 'formset': formset})

def delinv(req,pk):
    inv = Invoice.objects.get(pk=pk)
    inv.delete()
    return redirect('sales:invoice_list')



    