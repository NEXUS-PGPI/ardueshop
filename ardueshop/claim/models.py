from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Claim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    description = models.TextField()
    state = models.CharField(max_length=20, default='Pendiente')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reclamacion #{self.id} - {self.user.username}'