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
from apps.base.views import (
    HomeView
)

from allauth.account.views import LogoutView
from apps.accounts.views import LoginCustom,SignupCustom


urlpatterns = [
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tai-khoan/', include('allauth.urls')),
    url(r'^dang-nhap/$', LoginCustom.as_view(), name='login_custom'),
    url(r'^dang-ky/$', SignupCustom.as_view(), name='signup_custom'),
    url(r'^thoat-tai-khoan/$', LogoutView.as_view(), name='logout_custom'),

    url(r'^san-pham/$', ProductListView.as_view(), name='products'),
    url(r'^san-pham/(?P<slug>\d+)/$', ProductDetailView.as_view(), name='product_detail'),

    url(r'^loai-san-pham/(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='category_detail'),

    url(r'^danh-sach-don-hang/$', OrderList.as_view(), name='orders'),
    url(r'^chi-tiet-don-hang/(?P<order_number>\d+)/$', OrderDetail.as_view(), name='order_detail'),

    url(r'^gio-hang/$', CartView.as_view(), name='cart'),
    url(r'^gio-hang/so-luong/$', ItemCountView.as_view(), name='item_count'),

    url(r'^dat-hang/$', CheckoutView.as_view(), name='checkout'),
    url(r'^thanh-toan/$', CheckoutFinalView.as_view(), name='checkout_final'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
