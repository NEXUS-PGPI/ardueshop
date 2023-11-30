from django import forms
from .models import Claim

class ClaimForm(forms.ModelForm):
    
    type = forms.CharField(
      max_length=254,
      label="Tipo",
      widget=forms.TextInput(
        attrs={
          "placeholder": "Tipo de reclamacion",
          "class": "form-control"
        }
      )
    )
    description = forms.CharField(
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
        fields = ['type', 'description']
