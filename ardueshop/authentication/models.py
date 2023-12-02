from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ArduUser(User):

  # user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
  address = models.CharField(max_length=254)
  postal_code = models.DecimalField(max_digits=5, decimal_places=0)

  def __str__(self):
    return self.user.username.split("@")[0]