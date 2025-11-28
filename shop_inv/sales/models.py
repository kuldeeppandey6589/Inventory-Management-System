from django.db import models, transaction
from decimal import Decimal, ROUND_HALF_UP  
from catalog.models import Product
from inventory.models import StockMovement

class Customer(models.Model):
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=20, blank=True)
    address=models.TextField(blank=True)
    gstin=models.CharField(max_length=15, blank=True, help_text='Optional GSTIN')
    def __str__(self): return self.name
    
class Invoice(models.Model):
    number=models.CharField(max_length=50, unique=True, blank=True)
    date=models.DateTimeField(auto_now_add=True)
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True, blank=True)
    is_interstate=models.BooleanField(default=False, help_text='If checked, IGST; else CGST+SGST')
    subtotal=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cgst=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sgst=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    igst=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    def __str__(self): return self.number or f"Invoice {self.pk}"
    def _generate_number(self):
        from datetime import date
        today=date.today()
        fy_start=today.year if today.month>=4 else today.year-1
        fy=f"{fy_start}-{str(fy_start+1)[-2:]}"
        base=f"INV/{fy}/"
        last=Invoice.objects.filter(number__startswith=base).order_by('id').last()
        seq=1
        if last and last.number:
            try: seq=int(last.number.split('/')[-1])+1
            except Exception: seq=last.id+1
        return f"{base}{seq:06d}"
    
    def compute_totals(self):
        subtotal=Decimal('0.00'); cgst=Decimal('0.00'); sgst=Decimal('0.00'); igst=Decimal('0.00')
        for line in self.lines.all():
            line_total=(line.unit_price*line.qty)-(line.discount_amount or 0)
            if line_total < 0: line_total=Decimal('0.00')
            subtotal+=line_total
            rate=(line.product.gst_rate or Decimal('0'))/Decimal('100')
            tax=(line_total*rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            if self.is_interstate: igst+=tax
            else:
                half=(tax/2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                cgst+=half; sgst+=half
        grand=(subtotal+cgst+sgst+igst).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.subtotal=subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.cgst=cgst; self.sgst=sgst; self.igst=igst; self.grand_total=grand
    def save(self, *args, **kwargs):
        creating = self.pk is None
        if creating and not self.number: self.number=self._generate_number()
        super().save(*args, **kwargs)
    def post(self):
        with transaction.atomic():
            self.compute_totals(); super(Invoice,self).save()
            for line in self.lines.all():
                StockMovement.objects.create(product=line.product, qty=-int(line.qty), reason='SALE', reference=self.number)
class InvoiceLine(models.Model):
    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE, related_name='lines')
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    qty=models.PositiveIntegerField(default=1)
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self): return f"{self.product} x {self.qty}"

class buyer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.IntegerField(max_length=10)
    def __str__(self): return f"{self.name} x {self.phone}"
    
    