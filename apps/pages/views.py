from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, View,TemplateView
from apps.products.models import Product,Category
from .forms import ContactForm


class HomeView(View):
    template_name = "theme_lotus/pages/home.html"
    def get(self, request, *args, **kwargs):
        context = {}
        context['sections'] = []
        categories = Category.objects.filter(active=True)
        for category in categories:
            products = Product.objects.filter(default=category)[:8]
            if self.request.user and (self.request.user.is_superuser or self.request.user.is_staff):
                pass
            else:
                products.filter(active=True)
            context['sections'].append({"cat":category.title,"products":products})
        return render(request,self.template_name,context)


class IntroductionView(TemplateView):
    template_name = 'theme_lotus/pages/introduction.html'
class ContactView(TemplateView):
    template_name = 'theme_lotus/pages/contact.html'
class PaymentView(TemplateView):
    template_name = 'theme_lotus/pages/payment.html'
