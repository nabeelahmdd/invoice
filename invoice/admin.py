from django.contrib import admin
from invoice.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.options import ModelAdmin

# Register your models here.


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'weight', 'rate', 'making_charges', 'tax')
    list_filter = ('cr_at', 'up_at')
    search_fields = ('name', 'rate',)
    
admin.site.register(Product, ProductAdmin)


class InvoiceResource(resources.ModelResource):
    class Meta:
        model = Invoice

class InvoiceAdmin(ImportExportModelAdmin):
    resource_class = InvoiceResource
    list_display = ('name',)
    list_filter = ('cr_at', 'up_at')
    search_fields = ('mobile',)
    
admin.site.register(Invoice, InvoiceAdmin)