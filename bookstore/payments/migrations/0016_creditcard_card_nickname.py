# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0015_creditcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='card_nickname',
            field=models.CharField(default=None, max_length=150),
        ),
    ]
