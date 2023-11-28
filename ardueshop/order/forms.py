from django import forms
from .models import Order


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
