# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 16:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercheckout',
            name='email',
        ),
    ]