from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import random




from rest_framework import filters
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView

# Create your views here.
from .mixins import FilterMixin
from .filters import ProductFilter
from .forms import  ProductFilterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category
from .pagination import ProductPagination, CategoryPagination
from .serializers import (
		CategorySerializer, 
		ProductSerializer,
		 ProductDetailSerializer, 
		 ProductDetailUpdateSerializer
		)





# API ---
class APIHomeView(APIView):
	# authentication_classes = [SessionAuthentication]
	# permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		data = {
			"auth": {
				"login_url":  api_reverse("auth_login_api", request=request),
				"refresh_url":  api_reverse("refresh_token_api", request=request), 
				"user_checkout":  api_reverse("user_checkout_api", request=request), 
			},
			"address": {
				"url": api_reverse("user_address_list_api", request=request),
				"create":   api_reverse("user_address_create_api", request=request),
			},
			"checkout": {
				"cart": api_reverse("cart_api", request=request),
				"checkout": api_reverse("checkout_api", request=request),
				"finalize": api_reverse("checkout_finalize_api", request=request),
			},
			"products": {
				"count": Product.objects.all().count(),
				"url": api_reverse("products_api", request=request)
			},
			"categories": {
				"count": Category.objects.all().count(),
				"url": api_reverse("categories_api", request=request)
			},
			"orders": {
				"url": api_reverse("orders_api", request=request),
			}
		}
		return Response(data)




class CategoryListAPIView(generics.ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	pagination_class = CategoryPagination


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
	#authentication_classes = [SessionAuthentication]
	#permission_classes = [IsAuthenticated]
	queryset = Category.objects.all()
	serializer_class = CategorySerializer


class ProductListAPIView(generics.ListAPIView):
	#permission_classes = [IsAuthenticated]
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	filter_backends = [
					filters.SearchFilter, 
					filters.OrderingFilter, 
					filters.DjangoFilterBackend
					]
	search_fields = ["title", "description"]
	ordering_fields  = ["title", "id"]
	filter_class = ProductFilter
	#pagination_class = ProductPagination


class ProductRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDetailSerializer


# class ProductCreateAPIView(generics.CreateAPIView):
# 	queryset = Product.objects.all()
# 	serializer_class = ProductDetailUpdateSerializer



# WEB --------------------------------------------





class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = "theme_default/products/product_list.html"


class CategoryDetailView(DetailView):
	model = Category
	template_name = "theme_default/products/category_detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = ( product_set | default_products ).distinct()
		context["products"] = products
		return context

class ProductListView(FilterMixin, ListView):
	model = Product
	queryset = Product.objects.all()
	filter_class = ProductFilter
	template_name = "theme_default/products/product_list.html"


	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get("q") #None
		context["filter_form"] = ProductFilterForm(data=self.request.GET or None)
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs



class ProductDetailView(DetailView):
	model = Product
	template_name = "theme_default/products/product_detail.html"
	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		instance = self.get_object()
		context["related"] = sorted(Product.objects.get_related(instance)[:6], key= lambda x: random.random())
		return context




