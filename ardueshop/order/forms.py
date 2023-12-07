from django import forms
from .models import Order, Claim


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "email",
            "first_name",
            "last_name",
            "address",
            "postal_code",
            "city",
            "shipping_method",
            "payment_method",
        ]
        labels = {
            "email": "Correo Electrónico",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "address": "Dirección",
            "postal_code": "Código Postal",
            "city": "Ciudad",
            "shipping_method": "Método de entrega",
            "payment_method": "Método de Pago",
        }


class EmailPickerForm(forms.Form):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Correo Electrónico",
                "class": "form-control",
            }
        ),
    )


class ClaimForm(forms.ModelForm):
    comment = forms.CharField(
        max_length=254,
        label="Descripcion",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Descripcion de la reclamacion",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Claim
        fields = ["comment"]

class ClaimResponseForm(forms.ModelForm):
    response = forms.CharField(
        max_length=1024,
        label="Respuesta",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Respuesta a la reclamación",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Claim
        fields = ["response"]
