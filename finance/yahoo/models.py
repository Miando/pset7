from __future__ import unicode_literals

from django.db import models


class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    shares = models.CharField(max_length=250)
    price = models.CharField(max_length=250)

    def __str__(self):
        return self.symbol

class history:
    transaction = models.CharField(max_length=10)

