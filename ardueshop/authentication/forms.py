from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms

# Formularios de acceso y registro al sistema

class ClientCreationForm(UserCreationForm):

  username = forms.EmailField(
		max_length=254,
    label="Correo electrónico",
		widget=forms.EmailInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control"
			}
		)
	)

  password1 = forms.CharField(
    max_length=254,
    min_length=5,
    label="Contraseña",
    widget=forms.PasswordInput(
      attrs={
        "placeholder": "Contraseña",
        "class": "form-control"
      }
    )
  )

  password2 = forms.CharField(
    label="Confirme la contraseña",
    widget=forms.PasswordInput(
      attrs={
        "placeholder": "Contraseña",
        "class": "form-control"
      }
    )
  )

  class Meta:
    model = User
    fields = ('username', 'password1', 'password2')


class ClientLoginForm(AuthenticationForm):

  username = forms.EmailField(
    max_length=254,
    label="Correo electrónico",
		widget=forms.EmailInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control"
			}
		)
  )

  password = forms.CharField(
    max_length=254,
    min_length=5,
    label="Contraseña",
    widget=forms.PasswordInput(
      attrs={
        "placeholder": "Contraseña",
        "class": "form-control"
      }
    )
  )

  class Meta:
    model = User
    fields = ('username', 'password')