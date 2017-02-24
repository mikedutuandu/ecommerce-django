from django.contrib.auth.models import User
from django.db import models
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField
from django.db.models.signals import post_save
from config.utils import create_slug


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
    fullname = models.CharField(max_length=120,null=True)
    phone = models.CharField(max_length=120,null=True)
    city = models.CharField(max_length=120,null=True)
    district = models.CharField(max_length=120,null=True)
    wards = models.CharField(max_length=120,null=True)
    street = models.CharField(max_length=120,null=True)

    def __unicode__(self):
        return self.street

    def __str__(self):
        return self.street

    def get_address(self):
        return "%s, %s, %s %s" % (self.street, self.wards, self.district, self.city)


def post_save_user_receiver(sender, instance, *args, **kwargs):
    user = instance
    if UserProfile.objects.filter(user = user).count() == 0:
        UserProfile.objects.create(user=instance).save()
    if UserAddress.objects.filter(user=user).count() == 0:
        UserAddress.objects.create(user=instance).save()


post_save.connect(post_save_user_receiver, sender=User)
