# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20170626_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]