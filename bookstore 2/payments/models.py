# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class CreditCard(models.Model):
    cc_number = models.CharField(primary_key=True, max_length=255)
    security_code = models.CharField(max_length=3)
    expiration = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.cc_number

    class Meta:
        managed = True
        db_table = 'credit_cards'


