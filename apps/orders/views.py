from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, redirect,reverse
from django.views.generic.edit import CreateView, FormView,View,TemplateResponseMixin,ContextMixin
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView

import braintree

from django.conf import settings

from .forms import UserAddressForm
from .mixins import CartOrderMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  UserCheckout, Order
from apps.carts.models import Cart

User = get_user_model()

if settings.DEBUG:
	braintree.Configuration.configure(braintree.Environment.Sandbox,
      merchant_id=settings.BRAINTREE_MERCHANT_ID,
      public_key=settings.BRAINTREE_PUBLIC,
      private_key=settings.BRAINTREE_PRIVATE)

class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "theme_default/orders/order_detail.html"


class OrderList(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()
    template_name = "theme_default/orders/order_list.html"

    def get_queryset(self):
        user_checkout = UserCheckout.objects.get(user=self.request.user)
        return super(OrderList, self).get_queryset().filter(user=user_checkout)


class CheckoutView(CartOrderMixin, DetailView):
    model = Cart
    template_name = "theme_default/carts/checkout_view.html"

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart == None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        if self.request.user.is_authenticated():
            user_can_continue = True
            user_checkout, created = UserCheckout.objects.get_or_create(user=self.request.user)
            user_checkout.save()
            context["client_token"] = user_checkout.get_client_token()
            self.request.session["user_checkout_id"] = user_checkout.id
        else:
            context["next_url"] = self.request.build_absolute_uri()

        context["order"] = self.get_order()
        context["user_can_continue"] = user_can_continue
        return context

    def get_success_url(self):
        return reverse("checkout")

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        if cart == None:
            return redirect("cart")
        new_order = self.get_order()
        user_checkout_id = request.session.get("user_checkout_id")
        if user_checkout_id != None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            if new_order.order_address == None:
                return redirect("order_address")
            new_order.user = user_checkout
            new_order.save()
        return get_data


class CheckoutFinalView(CartOrderMixin, View):
    def post(self, request, *args, **kwargs):
        order = self.get_order()
        order_total = order.order_total
        nonce = request.POST.get("payment_method_nonce")
        if nonce:
            result = braintree.Transaction.sale({
                "amount": order_total,
                "payment_method_nonce": nonce,
                "billing": {
                    "postal_code": "%s" % (700000),

                },
                "options": {
                    "submit_for_settlement": True
                }
            })
            if result.is_success:
                # result.transaction.id to order
                order.mark_completed(order_id=result.transaction.id)
                messages.success(request, "Thank you for your order.")
                del request.session["cart_id"]
                del request.session["order_id"]
            else:
                # messages.success(request, "There was a problem with your order.")
                messages.success(request, "%s" % (result.message))
                return redirect("checkout")

        return redirect("order_detail", pk=order.pk)

    def get(self, request, *args, **kwargs):
        return redirect("checkout")


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


class AddressSelectView(CartOrderMixin,TemplateResponseMixin,ContextMixin,View):
    template_name = "theme_default/orders/address_select.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.useraddress == None:
            messages.success(self.request, "Please add a shipping address before continuing")
            return redirect("user_address_create")
        else:
            return super(AddressSelectView, self).dispatch(*args, **kwargs)


    def post(self,request):
        pass
    def get_success_url(self, *args, **kwargs):
        return "/checkout/"
