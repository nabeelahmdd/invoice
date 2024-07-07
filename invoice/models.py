from django.db import models
from decimal import Decimal
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=250)
    weight = models.DecimalField(max_digits=6, decimal_places=2)  # In grams
    rate = models.DecimalField(max_digits=8, decimal_places=2)    # Price per gram
    making_charges = models.DecimalField(max_digits=8, decimal_places=2)
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    soft_delete = models.BooleanField(default=False)
    cr_at = models.DateTimeField(auto_now_add=True)
    up_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        return self.price


class Invoice(models.Model):
    
    name = models.CharField(max_length=250, default="")
    mobile = models.CharField(max_length=15, default="")
    address = models.CharField(max_length=150, default="")
    country = models.CharField(max_length=150, default="India")
    state = models.CharField(max_length=150,default= "Madhya Pradesh")
    city = models.CharField(max_length=150, default="Burhanpur")
    zip_code = models.CharField(max_length=7, default="450331")

    products = models.ManyToManyField(Product)
    making_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    soft_delete = models.BooleanField(default=False)
    cr_at = models.DateTimeField(auto_now_add=True)
    up_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Invoice {self.id}"
    

    @property
    def advance_payment_total(self):
        return self.advancepayment_set.aggregate(total=models.Sum('price'))['total'] or 0



class AdvancePayment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    soft_delete = models.BooleanField(default=False)
    cr_at = models.DateTimeField(auto_now_add=True)
    up_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice.id} - {self.cr_at.strftime('%Y-%m-%d')}"