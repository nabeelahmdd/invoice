from django import forms
from invoice.models import *

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = [
            'name', 'mobile', 'address', 'country', 
            'state', 'city', 'zip_code'
        ]
