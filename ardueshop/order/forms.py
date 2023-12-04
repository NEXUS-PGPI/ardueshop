from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["email", "first_name", "last_name", "address", "postal_code", "city"]
        labels = {
            "email": "Correo Electrónico",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "address": "Dirección",
            "postal_code": "Código Postal",
            "city": "Ciudad",
        }
