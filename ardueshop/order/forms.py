from django import forms
from .models import Order, Claim


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["email", "address", "postal_code", "city"]
        labels = {
            "email": "Correo Electrónico",
            "address": "Dirección",
            "postal_code": "Código Postal",
            "city": "Ciudad",
        }

class ClaimForm(forms.ModelForm):
    
    comment = forms.CharField(
      max_length=254,
      label='Descripcion', 
      widget=forms.TextInput(
        attrs={
          "placeholder": "Descripcion de la reclamacion",
          "class": "form-control"
        }
      )
    )

    class Meta:
        model = Claim
        fields = ['comment']