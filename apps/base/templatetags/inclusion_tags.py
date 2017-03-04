
from django import template
from apps.products.models import Product,Category
from apps.carts.models import Cart,CartItem

register = template.Library()

@register.inclusion_tag('theme_lotus/base/inclusion_tags/_hot_products.html')
def hot_products():
    products = Product.objects.filter(hot=True,active=True)[:5]
    return {'products':products}

@register.inclusion_tag('theme_lotus/base/inclusion_tags/_left_nav.html')
def left_nav():
    categories = Category.objects.filter(active=True)
    return {'categories':categories}

@register.inclusion_tag('theme_lotus/base/inclusion_tags/_latest_post.html')
def latest_post():
    return {}

@register.inclusion_tag('theme_lotus/base/inclusion_tags/_head_card.html')
def head_card(request):
    cart_id = request.session.get("cart_id")
    if cart_id:
        cart = Cart.objects.get(id= cart_id)
    else:
        cart = None
    return {'cart':cart}

@register.inclusion_tag('theme_lotus/base/inclusion_tags/_head_search.html')
def head_search(request):
    categories = Category.objects.filter(active=True)
    return {'categories':categories,'cat':request.GET.get('cat',''),'q':request.GET.get('q','')}

@register.inclusion_tag('theme_lotus/base/inclusion_tags/_user_nav.html')
def user_nav():
    return {}


