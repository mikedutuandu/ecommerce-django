from django.core.urlresolvers import reverse
from django.db import models
from django.utils.safestring import mark_safe
from imagekit.processors import ResizeToFill, Thumbnail
from imagekit.models import ImageSpecField
from django.db.models.signals import pre_save
from config.utils import create_slug
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from apps.comments.models import Comment



class ProductManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(ProductManager, self).filter(active=True)

    def get_related(self, instance):
        products_one = super(ProductManager, self).filter(categories__in=instance.categories.all(), active=True)
        products_two = super(ProductManager, self).filter(default=instance.default, active=True)
        qs = (products_one | products_two).exclude(id=instance.id).distinct()
        return qs


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    short_description = models.TextField(blank=True,null=True)
    description = RichTextUploadingField()
    root_price = models.DecimalField(decimal_places=2, max_digits=20)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    inventory = models.IntegerField(null=True, blank=True)  # refer none == unlimited amount
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', blank=True)
    default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)
    hot = models.BooleanField(default=False)
    objects = ProductManager()

    class Meta:
        ordering = ["-title"]

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def get_image_url(self):
        img = self.productimage_set.first()
        if img:
            return img.image.url
        return img  # None
    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_html_price(self):
        if self.sale_price is not None:
            html_text = "<span class='price'>%s</span> <span class='price-before-discount'>%s</span>" % (
            self.sale_price, self.price)
        else:
            html_text = "<span class='price'>%s</span>" % (self.price)
        return mark_safe(html_text)
    def get_html_price_on_detail(self):
        if self.sale_price is not None:
            html_text = "<span class='price'>%s</span> <span class='price-strike'>%s</span>" % (
            self.sale_price, self.price)
        else:
            html_text = "<span class='price'>%s</span>" % (self.price)
        return mark_safe(html_text)

    def add_to_cart(self):
        return "%s?item=%s&qty=1" % (reverse("cart"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" % (reverse("cart"), self.id)

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs




def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_product_receiver, sender=Product)



def image_upload_to(instance, filename):
    return "products/%s" % (filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)
    image_thumb1 = ImageSpecField(source='image',
                                  processors=[ResizeToFill(41, 41)],
                                  format='JPEG',
                                  options={'quality': 100})
    image_thumb2 = ImageSpecField(source='image',
                                  processors=[ResizeToFill(68, 68)],
                                  format='JPEG',
                                  options={'quality': 100})
    image_thumb3 = ImageSpecField(source='image',
                                  processors=[ResizeToFill(90, 90)],
                                  format='JPEG',
                                  options={'quality': 100})
    image_thumb4 = ImageSpecField(source='image',
                                  processors=[ResizeToFill(150, 150)],
                                  format='JPEG',
                                  options={'quality': 100})
    image_thumb5 = ImageSpecField(source='image',
                                  processors=[ResizeToFill(189, 189)],
                                  format='JPEG',
                                  options={'quality': 100})
    image_thumb6 = ImageSpecField(source='image',
                                  processors=[ResizeToFill(317, 317)],
                                  format='JPEG',
                                  options={'quality': 100})
    image_thumb7 = ImageSpecField(source='image',
                                  processors=[ResizeToFill(700, 700)],
                                  format='JPEG',
                                  options={'quality': 100})

    def __unicode__(self):
        return self.product.title

    def __str__(self):
        return self.product.title


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_category_receiver, sender=Category)
