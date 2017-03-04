from allauth.account.views import LogoutView,LoginView,SignupView
from django.views.generic import UpdateView
from .models import UserAddress
from .forms import UserAddressForm
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginCustomView(LoginView):
    template_name = 'theme_lotus/accounts/login_view.html'

class SignupCustomView(SignupView):
    template_name = 'theme_lotus/accounts/signup_view.html'

class UserAddressView(LoginRequiredMixin,UpdateView):
    model = UserAddress
    form_class = UserAddressForm
    template_name = 'theme_lotus/accounts/user_address.html'
    success_url = '/dia-chi-cua-toi/'
    def get_object(self, queryset=None):
        return self.request.user.useraddress
