from django.shortcuts import render
from django.views import generic
from invoice.models import *
from invoice.forms import *
from django.utils import timezone
from django.http import JsonResponse
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from mysite.permission import SuperuserRequiredMixin
# Create your views here.

class InvoiceCreateUpdateView(
	LoginRequiredMixin,
	generic.View
):
	def get(self, request, *args, **kwargs):
		template_name = 'invoice/create.html'
		context = {
            'current_time': timezone.now(),
            'last_invoice': Invoice.objects.last()
        }
		if 'pk' in self.kwargs:
			template_name = 'invoice/update.html'
			context['object'] = Invoice.objects.filter(id=self.kwargs['pk']).last()
		return render(request, template_name, context)

	def  post(self, request, *args, **kwargs):
		try:

			if 'pk' in self.kwargs:
				success_msg = 'Invoice is updated successfully'
				instance = Invoice.objects.filter(pk=self.kwargs['pk']).last()
				form = InvoiceForm(request.POST, request.FILES, instance=instance)

			else:
				success_msg = 'Invoice is created successfully'
				form = InvoiceForm(request.POST, request.FILES)
				
			if form.is_valid():
				instance = form.save()
				data = json.loads(request.POST.get('jsonData'))
				
				for i in data:
					product = Product.objects.create(**i)
					instance.products.add(product)

				response = {
					'code': 1,
					'msg': success_msg,
					'redirect': '/',
				}
				return JsonResponse(response)

			else:
				for key, error in form.errors.items():
					if "required" in error[0]:
						message = '{0} is required'.format(key.replace('_', ' ').title())
					else:
						message = error

					response = {
					'code': 0,
					'msg': message,
					}
					return JsonResponse(response)

		except Exception as e:
			print(e)
			message = str(e)
			code = 0
		response = {
			'code': code,
			'msg': message,
		}
		return JsonResponse(response)


class InvoiceDetailView(
	LoginRequiredMixin,
	generic.DeleteView
):
	queryset = Invoice.objects.filter(soft_delete=False)
	template_name = 'invoice/detail.html'



class InvoiceDeleteView(
	SuperuserRequiredMixin,
	generic.View
):

	def  post(self, request, *args, **kwargs):
		try:
			instance = Invoice.objects.filter(pk=self.kwargs['pk'])
			instance.delete()
			message = 'Invoice is deleted successfully'
			code = 1

		except Exception as e:
			message = str(e)
			code = 0
		response = {
			'code': code,
			'msg': message,
			'redirect': '/'
		}
		return JsonResponse(response)


class ProductDeleteView(
	SuperuserRequiredMixin,
	generic.View
):

	def  post(self, request, *args, **kwargs):
		try:
			instance = Product.objects.filter(pk=self.kwargs['pk'])
			instance.delete()
			message = 'Product is deleted successfully'
			code = 1

		except Exception as e:
			message = str(e)
			code = 0
		response = {
			'code': code,
			'msg': message,
		}
		return JsonResponse(response)
