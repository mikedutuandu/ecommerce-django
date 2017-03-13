
from django import template
from apps.products.models import Product,Category
from apps.carts.models import Cart,CartItem
from apps.posts.models import Post

register = template.Library()

@register.inclusion_tag('theme_lotus/pages/inclusion_tags/_hot_products.html')
def hot_products():
    products = Product.objects.filter(hot=True,active=True)[:5]
    return {'products':products}

@register.inclusion_tag('theme_lotus/pages/inclusion_tags/_left_nav.html')
def left_nav(request):
    categories = Category.objects.filter(active=True).order_by('order')
    return {'categories':categories,'request':request}

@register.inclusion_tag('theme_lotus/pages/inclusion_tags/_latest_post.html')
def latest_post():
    posts = Post.objects.filter(active=True).order_by('-timestamp')[:3]
    return {'posts':posts}

@register.inclusion_tag('theme_lotus/pages/inclusion_tags/_head_card.html')
def head_card(request):
    cart_id = request.session.get("cart_id")
    if cart_id:
        cart = Cart.objects.get(id= cart_id)
    else:
        cart = None
    return {'cart':cart}

@register.inclusion_tag('theme_lotus/pages/inclusion_tags/_head_search.html')
def head_search(request):
    categories = Category.objects.filter(active=True)
    return {'categories':categories,'request':request}

@register.inclusion_tag('theme_lotus/pages/inclusion_tags/_user_nav.html')
def user_nav():
    return {}


