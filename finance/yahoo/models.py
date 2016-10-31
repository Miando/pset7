from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.db import models


class Stock(models.Model):
    user = models.ForeignKey(User, default=1)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    shares = models.CharField(max_length=250)
    price = models.CharField(max_length=250)

    def __str__(self):
        return self.symbol

class History(models.Model):
    user = models.ForeignKey(User, default=1)
    transaction = models.CharField(max_length=10)
    data = models.DateField()
    symbol = models.CharField('symbol', max_length=10)
    shares = models.CharField(max_length=250)
    price = models.CharField(max_length=250)

    def __str__(self):
        return self.transaction + " " + self.symbol

class Cash(models.Model):
    user = models.ForeignKey(User, default=1)
    money = models.CharField(max_length=250, default="10000")

    def __str__(self):
        return self.money