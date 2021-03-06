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
    HomeView,
    ContactView,
    IntroductionView,
    PaymentView
)
from apps.comments.views import CreateCommentView

from allauth.account.views import LogoutView
from apps.accounts.views import LoginCustomView, SignupCustomView, UserAddressView, UserProfileView
from apps.posts.views import PostDetailView, PostListView
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from apps.pages.views import PostSitemap,ProductSitemap,CategoryProductSitemap,StaticSitemap

sitemaps = {
    'post':PostSitemap,
    'product':ProductSitemap,
    'category-product':CategoryProductSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^tai-khoan/', include('allauth.urls')),

    url(r'^dang-nhap/$', LoginCustomView.as_view(), name='login_custom'),
    url(r'^dang-ky/$', SignupCustomView.as_view(), name='signup_custom'),
    url(r'^dia-chi-cua-toi/$', UserAddressView.as_view(), name='user_address'),
    url(r'^thong-tin-tai-khoan/$', UserProfileView.as_view(), name='user_profile'),
    url(r'^thoat-tai-khoan/$', LogoutView.as_view(), name='logout_custom'),

    url(r'^ve-tay-nguyen/$', PostListView.as_view(), name='post_list'),
    url(r'^ve-tay-nguyen/(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name='post_detail'),

    url(r'^lien-he/$', ContactView.as_view(), name='base_contact'),
    url(r'^gioi-thieu/$', IntroductionView.as_view(), name='base_introduction'),
    url(r'^hinh-thuc-thanh-toan/$', PaymentView.as_view(), name='base_payment'),

    url(r'^nhan-xet/$', CreateCommentView.as_view(), name='create_comment'),

    url(r'^san-pham/$', ProductListView.as_view(), name='products'),
    url(r'^san-pham/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='product_detail'),

    url(r'^loai-san-pham/(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='category_detail'),

    url(r'^danh-sach-don-hang/$', OrderList.as_view(), name='orders'),
    url(r'^chi-tiet-don-hang/(?P<order_number>\d+)/$', OrderDetail.as_view(), name='order_detail'),

    url(r'^gio-hang/$', CartView.as_view(), name='cart'),
    url(r'^gio-hang/so-luong/$', ItemCountView.as_view(), name='item_count'),

    url(r'^dat-hang/$', CheckoutView.as_view(), name='checkout'),
    url(r'^thanh-toan/$', CheckoutFinalView.as_view(), name='checkout_final'),

    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
import debug_toolbar

urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
