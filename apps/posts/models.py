from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from config.utils import create_slug
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.sitemaps import ping_google




class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(active=True).select_related('user')
    def get_related(self, instance):
        posts = super(PostManager, self).filter(categories__in=instance.categories.all(), active=True)
        qs = posts.exclude(id=instance.id).distinct()
        return qs


def upload_location(instance, filename):
    return "posts/%s" %(filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag',blank=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location)
    image_thumb1 = ImageSpecField(source='image',
                                      processors=[ResizeToFill(808, 418)],
                                      format='JPEG',
                                      options={'quality': 100})
    image_thumb2 = ImageSpecField(source='image',
                                      processors=[ResizeToFill(223, 115)],
                                      format='JPEG',
                                      options={'quality': 100})
    image_thumb3 = ImageSpecField(source='image',
                                      processors=[ResizeToFill(408, 201)],
                                      format='JPEG',
                                      options={'quality': 100})
    short_content = models.TextField(blank=True, null=True)
    content = RichTextUploadingField()
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


    seo_title = models.CharField(max_length=250,null=True,blank=True)
    seo_description = models.TextField(null=True,blank=True)
    seo_keyword = models.TextField(max_length=250,null=True,blank=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
    
    class Meta:
        ordering = ["-timestamp", "-updated"]


    def save(self, force_insert=False, force_update=False):
        super(Post, self).save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)

class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    seo_title = models.CharField(max_length=250,null=True,blank=True)
    seo_description = models.TextField(null=True,blank=True)
    seo_keyword = models.TextField(max_length=250,null=True,blank=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_category_receiver, sender=Category)


class Tag(models.Model):
    name = models.CharField(max_length=120, unique=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name











