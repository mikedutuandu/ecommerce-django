
from allauth.account.adapter import DefaultAccountAdapter
# from django.contrib.auth.models import User

class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return '/checkout'