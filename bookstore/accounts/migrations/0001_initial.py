# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=255, unique=True)),
                ('email_address', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('home_address', models.CharField(max_length=255)),
            ],
            options={
                'managed': True,
                'db_table': 'users',
            },
        ),
    ]
