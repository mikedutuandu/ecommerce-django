from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
# Create your models here.
from apps.carts.models import Cart

import braintree

if settings.DEBUG:
    braintree.Configuration.configure(braintree.Environment.Sandbox,
                                      merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                      public_key=settings.BRAINTREE_PUBLIC,
                                      private_key=settings.BRAINTREE_PRIVATE)


class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)  # not required
    braintree_id = models.CharField(max_length=120, null=True, blank=True)

    def __unicode__(self):  # def __str__(self):
        return self.user.email

    def __str__(self):  # def __str__(self):
        return self.user.email

    @property
    def get_braintree_id(self, ):
        instance = self
        if not instance.braintree_id:
            result = braintree.Customer.create({
                "email": instance.user.email,
            })
            if result.is_success:
                instance.braintree_id = result.customer.id
                instance.save()
        return instance.braintree_id

    def get_client_token(self):
        customer_id = self.get_braintree_id
        if customer_id:
            client_token = braintree.ClientToken.generate({
                "customer_id": customer_id
            })
            return client_token
        return None


def update_braintree_id(sender, instance, *args, **kwargs):
    if not instance.braintree_id:
        instance.get_braintree_id


post_save.connect(update_braintree_id, sender=UserCheckout)

ORDER_STATUS_CHOICES = (

    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('completed', 'Completed'),
)
PAYMENT_METHOD_CHOICES = (

    ('order', 'Order'),
    ('braintree', 'Braintree')
)


class OrderAddress(models.Model):
    fullname = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    district = models.CharField(max_length=120)
    wards = models.CharField(max_length=120)
    street = models.CharField(max_length=120)

    def __unicode__(self):
        return self.street

    def __str__(self):
        return self.street

    def get_address(self):
        return "%s, %s, %s %s" % (self.street, self.wards, self.district, self.city)


class Order(models.Model):
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='draft')
    user_checkout = models.ForeignKey(UserCheckout, null=True)
    cart = models.ForeignKey(Cart)
    order_address = models.OneToOneField(OrderAddress, null=True)
    shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99)
    order_total = models.DecimalField(max_digits=50, decimal_places=2, )
    order_id = models.CharField(max_length=20, null=True, blank=True)
    payment_method = models.CharField(max_length=120, choices=PAYMENT_METHOD_CHOICES, default='order')
    order_number = models.IntegerField(unique=True, null=True)

    def __unicode__(self):
        return "Order_id: %s, Cart_id: %s" % (self.id, self.cart.id)

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"order_number": self.order_number})

    def mark_status(self, order_id=None):
        self.order_number = self.id + 1000000
        self.status = "pending"
        if order_id and not self.order_id:
            self.order_id = order_id
            self.payment_method = "braintree"
        self.save()

    @property
    def is_complete(self):
        if self.status == "completed":
            return True
        return False


def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total


pre_save.connect(order_pre_save, sender=Order)
