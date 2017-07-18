# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from datetime import datetime
from accounts.models import User
from products.models import Book
from django.db import models
from accounts.models import Address


class CreditCard(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cc_number = models.CharField(max_length=16)
    security_code = models.CharField(max_length=3)
    expiration = models.DateField()
    provider = models.CharField(max_length=50)
    name_on_card = models.CharField(max_length=150)

    def __str__(self):
        return self.user.email_address + " --> " + self.cc_number

    class Meta:
        managed = True
        db_table = 'credit_cards'


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    tax_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    date_ordered = models.DateTimeField(default=datetime.now, blank=True)
    payed_order = models.BooleanField(default=False)
    # add later an address field
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True, related_name='addresses')

    def __str__(self):
        return self.user.nickname + " Order Id : " + str(self.id)

    class Meta:
        managed = True
        db_table = 'orders'


class FutureOrder(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Future Order : " + self.user.nickname

    class Meta:
        managed = True
        db_table = 'future_orders'


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    book = models.ForeignKey(Book, related_name='book')
    quantity = models.IntegerField(default=1)
    payed_item = models.BooleanField(default=False)
    book_price_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return "Order Id : " + str(self.id) + " Order Item Id : " + str(self.id)

    class Meta:
        managed = True
        db_table = 'order_items'


class FutureOrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    future_order = models.ForeignKey(FutureOrder, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='future_book')

    def __str__(self):
        return "Future Order Item : " + self.book.title + " for " + self.future_order.user.nickname

    class Meta:
        managed = True
        db_table = 'future_order_items'






