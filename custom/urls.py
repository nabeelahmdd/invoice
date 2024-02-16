from django.urls import path
from custom.views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('user-profile/', SiteSettingView.as_view(), name='user-profile'),
    path('site-setting/', SiteSettingView.as_view(), name='site-setting'),
]