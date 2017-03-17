from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
import random
from .mixins import FilterMixin
from .filters import ProductFilter
from .forms import  ProductFilterForm
from .models import Product, Category

from apps.pages.models import Banner





class CategoryDetailView(DetailView):
	model = Category
	template_name = "theme_lotus/products/product_list.html"

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		product_set = obj.product_set.filter(active=True)
		default_products = obj.default_category.filter(active=True)
		products = ( product_set | default_products ).distinct()
		context["object_list"] = products
		context['banner'] = Banner.objects.filter(active=True, location='product').first()
		return context

class ProductListView(FilterMixin, ListView):
	model = Product
	queryset = Product.objects.all()
	filter_class = ProductFilter
	template_name = "theme_lotus/products/product_list.html"


	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get("q") #None
		context["filter_form"] = ProductFilterForm(data=self.request.GET or None)
		context['banner'] = Banner.objects.filter(active=True,location='product').first()
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		if not self.request.user.is_superuser and not self.request.user.is_staff:
			qs = self.model.objects.filter(active=True)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)
			if not self.request.user.is_superuser and not self.request.user.is_staff:
				qs = qs.filter(active=True)
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				if not self.request.user.is_superuser and not self.request.user.is_staff:
					qs = qs2.filter(active=True)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs



class ProductDetailView(DetailView):
	model = Product
	template_name = "theme_lotus/products/product_detail.html"
	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		instance = self.get_object()
		context["related"] = sorted(Product.objects.get_related(instance)[:8], key= lambda x: random.random())
		return context




