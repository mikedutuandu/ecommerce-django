from django.contrib import admin

# Register your models here.


from .models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = ('id','order','location','active')
    list_editable = ["order"]
    class Meta:
        model = Banner


admin.site.register(Banner, BannerAdmin)