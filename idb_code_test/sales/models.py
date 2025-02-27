from django.db import models


# Create your models here.
class Sale(models.Model):
    date = models.DateField()
    region = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
