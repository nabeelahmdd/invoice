from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from custom.models import (
    CustomUser, SiteSetting
)
# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
    	'email', 'first_name', 'last_name', 'phone_number',
    )
    search_fields = (
    	'email','first_name', 'last_name',  'phone_number',
    )
    list_filter = ('date_joined',)


admin.site.register(CustomUser, CustomUserAdmin)


class SiteSettingAdmin(admin.ModelAdmin):
    list_display = (
    	'title', 'nav_color', 'body_color',
    )
    search_fields = (
    	'title', 'nav_color', 'body_color',
    )


admin.site.register(SiteSetting, SiteSettingAdmin)