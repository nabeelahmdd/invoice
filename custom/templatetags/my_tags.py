from django import template
from custom.models import SiteSetting

register = template.Library()

@register.filter
def sitesetting(request):
    sitesetting = SiteSetting.objects.all().order_by('-id')[0:1]
    return sitesetting 