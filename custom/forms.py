from django import forms
from custom.models import SiteSetting

class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = '__all__'