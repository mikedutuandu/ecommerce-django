
from allauth.account.adapter import DefaultAccountAdapter
from django.core.urlresolvers import reverse

class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.session.get('order_id'):
            return reverse('checkout')
        return '/'