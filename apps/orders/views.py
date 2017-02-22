from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
# Create your views here.

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.carts.mixins import TokenMixin

from .forms import AddressForm, UserAddressForm
from .mixins import CartOrderMixin, UserCheckoutMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserAddress, UserCheckout, Order
from .permissions import IsOwnerAndAuth
from .serializers import UserAddressSerializer, OrderSerializer, OrderDetailSerializer

User = get_user_model()


# API --------------------------------

class UserCheckoutAPI(UserCheckoutMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        data = self.get_checkout_data(user=request.user)
        return Response(data)

    def post(self, request, format=None):
        data = {}
        email = request.data.get("email")
        if request.user.is_authenticated():
            if email == request.user.email:
                data = self.get_checkout_data(user=request.user, email=email)
            else:
                data = self.get_checkout_data(user=request.user)
        elif email and not request.user.is_authenticated():
            data = self.get_checkout_data(email=email)
        else:
            data = self.user_failure(message="Make sure you are authenticated or using a valid email.")
        return Response(data)

class OrderRetrieveAPIView(RetrieveAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsOwnerAndAuth]
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        return Order.objects.filter(user__user=self.request.user)


class OrderListAPIView(ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsOwnerAndAuth]
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        return Order.objects.filter(user__user=self.request.user)


class UserAddressCreateAPIView(CreateAPIView):
    model = UserAddress
    serializer_class = UserAddressSerializer


class UserAddressListAPIView(TokenMixin, ListAPIView):
    model = UserAddress
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    def get_queryset(self, *args, **kwargs):
        user_checkout_token = self.request.GET.get("checkout_token")
        user_checkout_data = self.parse_token(user_checkout_token)
        user_checkout_id = user_checkout_data.get("user_checkout_id")
        if self.request.user.is_authenticated():
            return UserAddress.objects.filter(user__user=self.request.user)
        elif user_checkout_id:
            return UserAddress.objects.filter(user__id=int(user_checkout_id))
        else:
            return []


# WEB -----------------------------------------




class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "theme_default/orders/order_detail.html"


class OrderList(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()
    template_name = "theme_default/orders/order_list.html"

    def get_queryset(self):
        user_checkout = UserCheckout.objects.get(user=self.request.user)
        return super(OrderList, self).get_queryset().filter(user=user_checkout)


class UserAddressCreateView(CreateView):
    form_class = UserAddressForm
    template_name = "theme_default/pages/forms.html"
    success_url = "/checkout/address/"

    def get_checkout_user(self):
        user_check_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return user_checkout

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.get_checkout_user()
        return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)


class AddressSelectFormView(CartOrderMixin, FormView):
    form_class = AddressForm
    template_name = "theme_default/orders/address_select.html"

    def dispatch(self, *args, **kwargs):
        b_address, s_address = self.get_addresses()
        if s_address.count() == 0:
            messages.success(self.request, "Please add a shipping address before continuing")
            return redirect("user_address_create")
        else:
            return super(AddressSelectFormView, self).dispatch(*args, **kwargs)

    def get_addresses(self, *args, **kwargs):
        user_check_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        b_address = UserAddress.objects.filter(
            user=user_checkout,
            type='billing',
        )
        s_address = UserAddress.objects.filter(
            user=user_checkout,
            type='shipping',
        )
        return b_address, s_address

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
        b_address, s_address = self.get_addresses()

        form.fields["shipping_address"].queryset = s_address
        return form

    def form_valid(self, form, *args, **kwargs):
        shipping_address = form.cleaned_data["shipping_address"]
        order = self.get_order()
        order.shipping_address = shipping_address
        order.save()
        return super(AddressSelectFormView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return "/checkout/"
