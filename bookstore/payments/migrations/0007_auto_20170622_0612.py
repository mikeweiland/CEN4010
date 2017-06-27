# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-22 06:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20170622_0413'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payed_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='payed_item',
            field=models.BooleanField(default=False),
        ),
    ]