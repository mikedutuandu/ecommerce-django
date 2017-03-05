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
            context['sections'].append({"cat":category.title,"products":products})
        return render(request,self.template_name,context)


class IntroductionView(TemplateView):
    template_name = 'theme_lotus/pages/introduction.html'
class ContactView(TemplateView):
    template_name = 'theme_lotus/pages/contact.html'
class PaymentView(TemplateView):
    template_name = 'theme_lotus/pages/payment.html'
