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


class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    district = models.CharField(max_length=120)
    wards = models.CharField(max_length=120)
    street = models.CharField(max_length=120)

    def __unicode__(self):
        return self.street

    def __str__(self):
        return self.street

    def get_address(self):
        return "%s, %s, %s %s" % (self.street, self.wards, self.district, self.city)
