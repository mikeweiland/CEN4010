# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0003_delete_creditcard'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('cc_number', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('security_code', models.CharField(max_length=3)),
                ('expiration', models.CharField(max_length=255)),
                ('provider', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
            ],
            options={
                'managed': True,
                'db_table': 'credit_cards',
            },
        ),
    ]