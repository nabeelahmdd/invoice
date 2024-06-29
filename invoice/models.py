from django.db import models

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
    is_active = models.BooleanField(default=True)
    soft_delete = models.BooleanField(default=False)
    cr_at = models.DateTimeField(auto_now_add=True)
    up_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Invoice {self.id} - {self.cr_at.strftime('%Y-%m-%d')}"

    @property
    def making_charges(self):
        return sum(product.making_charges for product in self.products.all())
    
    @property
    def tax(self):
        return sum(product.tax for product in self.products.all())
    
    @property
    def total(self):
        return sum(product.price for product in self.products.all())
    
    @property
    def subtotal(self):
        return self.total - self.making_charges - self.tax

