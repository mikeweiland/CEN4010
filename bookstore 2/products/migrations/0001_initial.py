# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 21:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('author_id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('bio', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('title', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('cover_file_name', models.CharField(blank=True, max_length=255, null=True)),
                ('genre', models.CharField(blank=True, max_length=7, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('author', models.IntegerField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('publisher', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TechValleyTimes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('book', models.ForeignKey(db_column='book', on_delete=django.db.models.deletion.DO_NOTHING, to='products.Books')),
            ],
        ),
    ]
