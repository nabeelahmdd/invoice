from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from custom.models import SiteSetting
from custom.forms import SiteSettingForm
from django.contrib import messages
from invoice.models import *
User = get_user_model()

# Create your views here.
class HomeView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10
    model = Invoice
    template_name = "home.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_field = self.request.GET.get('field')  # Field to filter by
        filter_value = self.request.GET.get('value')  # Value to filter by

        if filter_field and filter_value:
            filter_kwargs = {filter_field: filter_value}
            queryset = queryset.filter(**filter_kwargs)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_invoices'] = Invoice.objects.all().count()
        return context


class UserProfileView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView
):
    model = User
    fields = [
        'first_name', 'last_name', 'email', 'phone_number',
        'image', 'gender', 
    ]
    success_message = "Profile Has been Updated!"
    success_url = reverse_lazy("home")
    template_name = "account/profile.html"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)
    

class SiteSettingView(
    LoginRequiredMixin,
    generic.View):
    

    def get(self, request, *args, **kwargs):
        
        if not request.user.is_superuser:
            messages.error(request, 'Only Super user can access this page')
            return redirect('/')
        
        context = {
            'instance': SiteSetting.objects.last(),
        }
        return render(request, "site_setting.html", context)
    
    def post(self, request, *args, **kwargs):
        instance = SiteSetting.objects.last()
        if instance:
            form = SiteSettingForm(request.POST, request.FILES, instance=instance)
        else:
            form = SiteSettingForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Site setting has been updated")
        else:
            messages.error(request, 'Please correct the error below.')

        return redirect('/site-setting/')