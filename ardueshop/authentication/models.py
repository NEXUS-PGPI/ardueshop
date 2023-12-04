from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ArduUser(models.Model):

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  address = models.CharField(max_length=254, blank=True, null=True)
  postal_code = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
  city = models.CharField(max_length=254, blank=True, null=True)

  def __str__(self):
    return self.user.username.split("@")[0]