from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, View,TemplateView
from .models import Banner
from django.contrib.sitemaps import Sitemap
from apps.posts.models import Post
from apps.products.models import Product,Category
from django.urls import reverse


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
            context['sections'].append({"category":category,"products":products})
        return render(request,self.template_name,context)


class IntroductionView(TemplateView):
    template_name = 'theme_lotus/pages/introduction.html'
class ContactView(TemplateView):
    template_name = 'theme_lotus/pages/contact.html'
class PaymentView(TemplateView):
    template_name = 'theme_lotus/pages/payment.html'

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Post.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.updated

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Product.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.updated
class CategoryProductSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return Category.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.updated

class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home', 'login_custom', 'signup_custom',
                'user_address','user_profile','logout_custom','post_list'
                ,'base_contact','base_introduction','base_payment','products',
                'orders','cart'
                ]

    def location(self, item):
        return reverse(item)


