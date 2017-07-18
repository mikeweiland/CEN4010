# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.utils import timezone
from accounts.models import User
from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.CharField(max_length=2000)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        managed = True
        db_table = 'authors'


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=255)
    quantity = models.IntegerField(blank=True, null=True)
    cover_file_name = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=7, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'books'


class TechValleyTimes(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Tech Valley Times : " + self.book.title

    class Meta:
        managed = True
        db_table = 'tech_valley_times'


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, null=True)
    published_date = models.DateField(default=timezone.now)
    user_rating = models.DecimalField(max_digits=3, decimal_places=2)
    review_header = models.CharField(max_length=255)
    review_body = models.TextField()
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.review_header

    class Meta:
        managed = True
        db_table = 'reviews'

