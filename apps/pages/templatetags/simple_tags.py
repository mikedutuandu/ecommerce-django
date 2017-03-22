
from django import template

from apps.pages.models import Setting

register = template.Library()




@register.simple_tag
def get_setting(name):
    setting = Setting.objects.first()
    if setting:
        if name == 'phone_hn':
            return setting.phone_hn
        if name == 'phone_sg':
            return setting.phone_sg
        if name == 'email':
            return setting.email
        if name == 'facebook':
            return setting.facebook
        if name == 'youtube':
            return setting.youtube
        if name == 'domain':
            return setting.domain
        if name == 'logo':
            return setting.logo.url
        if name == 'address':
            return setting.address
        if name == 'skype':
            return setting.skype
        if name == 'text1':
            return setting.text1
        if name == 'text2':
            return setting.text2
        if name == 'text3':
            return setting.text3
    return ''