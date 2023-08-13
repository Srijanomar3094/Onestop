from django.db import models
from django.contrib.auth.models import User


class Inventory(models.Model):
    category = models.CharField(max_length=200)
    createdTime = models.DateTimeField(auto_now_add=True, null=True)
    updatedTime = models.DateTimeField(auto_now=True, null=True)
    deletedTime = models.DateTimeField(null=True, default=None)
    blob = models.ImageField(upload_to='onestop/grocery/inventory/')


class Product(models.Model):
    product = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    createdTime = models.DateTimeField(auto_now_add=True, null=True)
    updatedTime = models.DateTimeField(auto_now=True, null=True)
    deletedTime = models.DateTimeField(null=True, default=None)
    blob = models.ImageField(upload_to='onestop/grocery/inventory/')
    quantity = models.IntegerField(default=1)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    addedTime = models.DateTimeField(auto_now_add=True, null=True)
    updatedTime = models.DateTimeField(auto_now=True, null=True)
    deletedTime = models.DateTimeField(null=True, default=None)
    buystatus = models.BooleanField(default=False)
    totalprice = models.IntegerField(default=1)


class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    productid = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    billtotal = models.IntegerField(default=1)
    buyTime = models.DateTimeField(auto_now_add=True, null=True)
   

