from django.contrib.auth.models import User
from django.db import models
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField

def upload_location(instance, filename):
    return "accounts/%s" % (filename)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                                )
    avatar_thumb = ImageSpecField(source='avatar',
                                 processors=[ResizeToFill(40, 40)],
                                 format='JPEG',
                                 options={'quality': 60})

    def __unicode__(self):
        return ''

    def __str__(self):
        return ''