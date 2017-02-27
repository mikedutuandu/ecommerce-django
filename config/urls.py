from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from apps.products.views import ProductDetailView, ProductListView, \
    CategoryDetailView

from apps.carts.views import (
    CartView,
    ItemCountView,
)
from apps.orders.views import (
    OrderList,
    OrderDetail,
    CheckoutView,
    CheckoutFinalView,
)
from apps.pages.views import (
    HomeView
)


urlpatterns = [
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^san-pham/$', ProductListView.as_view(), name='products'),
    url(r'^san-pham/(?P<slug>\d+)/$', ProductDetailView.as_view(), name='product_detail'),

    url(r'^loai-san-pham/(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='category_detail'),

    url(r'^orders/$', OrderList.as_view(), name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),

    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),

    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/final/$', CheckoutFinalView.as_view(), name='checkout_final'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
