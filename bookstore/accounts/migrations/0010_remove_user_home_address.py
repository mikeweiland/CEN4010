# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-25 22:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20170625_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='home_address',
        ),
    ]
