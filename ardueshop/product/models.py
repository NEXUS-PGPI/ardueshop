from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    stock = models.BigIntegerField()
    price = models.FloatField()
    image = models.ImageField(null=True, upload_to='products/')
    category = models.ForeignKey(Category,
                                 on_delete= models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='products')
    
    def __str__(self):
        return self.name

class Opinion(models.Model):
    date = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opinions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='opinions')

    def __str__(self):
        return self.comment
