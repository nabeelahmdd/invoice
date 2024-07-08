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
from django.http import JsonResponse

User = get_user_model()

# Create your views here.
class HomeView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10
    model = Invoice
    template_name = "home.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.request.GET)
        filter_field = self.request.GET.get('field')  # Field to filter by
        filter_value = self.request.GET.get('value')  # Value to filter by

        if filter_field and filter_value:
            filter_kwargs = {f'{filter_field}__icontains': filter_value}
            queryset = queryset.filter(**filter_kwargs)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_invoices'] = Invoice.objects.all().count()
        print(context)
        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            invoices = list(context['object_list'].values(
                'id', 'name', 'mobile', 'address', 'total',
            ))
            pagination = {
                'is_paginated': context['is_paginated'],
                'current_page': context['page_obj'].number,
                'num_pages': context['paginator'].num_pages,
                'has_previous': context['page_obj'].has_previous(),
                'previous_page_number': context['page_obj'].previous_page_number() if context['page_obj'].has_previous() else None,
                'has_next': context['page_obj'].has_next(),
                'next_page_number': context['page_obj'].next_page_number() if context['page_obj'].has_next() else None,
                'page_range': list(context['paginator'].page_range),
            }
            return JsonResponse({'invoices': invoices, 'pagination': pagination})
        else:
            return super().render_to_response(context, **response_kwargs)

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