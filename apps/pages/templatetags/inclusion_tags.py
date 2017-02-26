
from django import template
from apps.products.models import Product,Category

register = template.Library()

@register.inclusion_tag('theme_lotus/pages/inclusion_tags/_hot_products.html')
def hot_products():
    products = Product.objects.filter(hot=True,active=True)[:5]
    return {'products':products}
@register.inclusion_tag('theme_lotus/pages/inclusion_tags/_left_nav.html')
def left_nav():
    categories = Category.objects.filter(active=True)
    return {'categories':categories}


