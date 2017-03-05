from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from config.utils import create_slug
from ckeditor_uploader.fields import RichTextUploadingField



class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(active=True).select_related('user')


def upload_location(instance, filename):
    return "posts/%s" %(filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
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
    short_content = models.TextField(blank=True, null=True)
    content = RichTextUploadingField()
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
    
    class Meta:
        ordering = ["-timestamp", "-updated"]



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)











