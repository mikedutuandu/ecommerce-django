from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from config.utils import create_slug
from ckeditor_uploader.fields import RichTextUploadingField


LOCATION_CHOICES = (

    ('home', 'HOME'),
    ('product', 'PRODUCT')
)
def upload_location(instance, filename):
    return "banners/%s" % (filename)
class Banner(models.Model):
    text1 = models.CharField(max_length=250,null=True,blank=True)
    text2 = models.CharField(max_length=250,null=True,blank=True)
    text3 = models.CharField(max_length=250,null=True,blank=True)
    image = models.ImageField(upload_to=upload_location)
    link = models.URLField(null=True,blank=True)
    order = models.IntegerField()
    location = models.CharField(max_length=120, choices=LOCATION_CHOICES, default='home')
    image_thumb1 = ImageSpecField(source='image',
                                  processors=[ResizeToFill(848, 430)],
                                  format='JPEG',
                                  options={'quality': 100})
    image_thumb2 = ImageSpecField(source='image',
                                  processors=[ResizeToFill(848, 359)],
                                  format='JPEG',
                                  options={'quality': 100})
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)











