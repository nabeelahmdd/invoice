from django.urls import path
from invoice.views import *

urlpatterns = [
    path('create/', InvoiceCreateUpdateView.as_view(), name='invoice-create'),
    path('edit/<int:pk>/', InvoiceCreateUpdateView.as_view(), name='invoice-edit'),
    path('detail/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('delete/<int:pk>/', InvoiceDeleteView.as_view(), name='invoice-delete'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
]