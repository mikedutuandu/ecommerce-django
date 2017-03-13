from django.contrib import admin
from django import forms

# Register your models here.


from .models import Product, ProductImage, Category


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 10


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'price']
    inlines = [
        ProductImageInline,
    ]
    fields = ['title', 'short_description', 'description', 'root_price', 'price', 'sale_price', 'inventory', 'active',
              'categories', 'default', 'hot']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(ProductAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

    def get_fields(self, request, obj=None):
        if not request.user.is_superuser:
            self.fields = ['title', 'short_description', 'description', 'root_price', 'inventory', 'categories',
                           'default']
        return super(ProductAdmin,self).get_fields(request, obj)

    class Meta:
        model = Product



admin.site.register(Product, ProductAdmin)


admin.site.register(Category)
