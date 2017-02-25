from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, redirect,reverse
from django.views.generic.edit import CreateView, UpdateView,View,TemplateResponseMixin,ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import ModelFormMixin
from  django.views.generic.list import ListView
from apps.accounts.models import UserAddress

import braintree

from django.conf import settings

from .forms import UserAddressForm
from .mixins import CartOrderMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  UserCheckout, Order,OrderAddress
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
        return super(OrderList, self).get_queryset().filter(user_checkout=user_checkout)


class CheckoutView(CartOrderMixin, View):
    template_name = "theme_default/carts/checkout_view.html"

    def get_context(self):
        user_can_continue = False
        context = {}
        if self.request.user.is_authenticated():
            user_can_continue = True
        context["order"] = self.get_order()
        context["user_can_continue"] = user_can_continue
        context['form'] = UserAddressForm(instance=self.request.user.useraddress)
        return context
    def update_order_address(self):
        order = self.get_order()
        user_address = self.request.user.useraddress
        order_address = OrderAddress.objects.create(
            fullname=user_address.fullname,
            city=user_address.city,
            district=user_address.district,
            wards=user_address.wards,
            phone=user_address.phone,
            street=user_address.street
        )
        order.order_address = order_address
        order.save()
    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):
        context = self.get_context()
        form = UserAddressForm(self.request.POST or None,self.request.FILES or None,instance=self.request.user.useraddress)
        if form.is_valid():
            form.save()
            self.update_order_address()
            context['form'] = form
            return redirect('checkout_final')
        else:
            context['form'] = form
        return render(request, self.template_name, context)


class CheckoutFinalView(LoginRequiredMixin,CartOrderMixin, View):
    template_name = "theme_default/carts/checkout_final_view.html"

    def get_context(self):
        context = {}
        user_checkout, created = UserCheckout.objects.get_or_create(user=self.request.user)
        user_checkout.save()
        order = self.get_order()
        order.user_checkout = user_checkout
        order.save()
        context["client_token"] = user_checkout.get_client_token()
        context["order"] = self.get_order()
        return context

    def get(self, request, *args, **kwargs):
        order = self.get_order()
        if not order.order_address:
            return redirect('checkout')
        context= self.get_context()
        return render(request,self.template_name,context)

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





