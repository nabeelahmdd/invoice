
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
User = get_user_model()
class ProfileCompleteMiddleware(MiddlewareMixin):

    def validate_user_data(self, request):
        user_data = User.objects.filter(id=request.user.id).values(
            'first_name', 'last_name', 'email', 'phone_number',
            'gender', 
        )
        error_msg = {}

        for item in user_data:
            for k, v in item.items():
                if None == v or v == '':
                    error_msg[k] = v
                    field_name = k.replace("_", " ").title()
                    messages.error(request, f'Please filled out {field_name}')
        return error_msg

    def process_request(self, request):
        path = ['/accounts/logout/', '/user-profile/',]

        if request.user.is_authenticated and \
            request.path not in path and \
            not request.user.is_superuser:
                incom_profile = self.validate_user_data(request)
                if incom_profile:
                    return redirect('/user-profile/')