from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, View,TemplateView
from apps.products.models import Product,Category
from .forms import ContactForm
from .models import Banner


class HomeView(View):
    template_name = "theme_lotus/pages/home.html"
    def get(self, request, *args, **kwargs):
        context = {}
        context['sections'] = []
        categories = Category.objects.filter(active=True)
        banners =Banner.objects.filter(active=True,location='home').order_by('order')
        context['banners'] = banners
        for category in categories:
            if self.request.user and (self.request.user.is_superuser or self.request.user.is_staff):
                products = Product.objects.filter(default=category)[:8]
            else:
                products = Product.objects.filter(active=True,default=category)[:8]
            context['sections'].append({"cat":category.title,"products":products})
        return render(request,self.template_name,context)


class IntroductionView(TemplateView):
    template_name = 'theme_lotus/pages/introduction.html'
class ContactView(TemplateView):
    template_name = 'theme_lotus/pages/contact.html'
class PaymentView(TemplateView):
    template_name = 'theme_lotus/pages/payment.html'
