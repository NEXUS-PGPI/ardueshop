from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from django.contrib.auth.models import User

# Formularios de acceso y registro al sistema

class ClientCreationForm(UserCreationForm):

  first_name = forms.CharField(
    max_length=254,
    label="Nombre",
    widget=forms.HiddenInput(),
    required=False
  )

  last_name = forms.CharField(
    max_length=254,
    label="Apellido",
    widget=forms.HiddenInput(),
    required=False
  )

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

  email = forms.EmailField(
    widget=forms.HiddenInput(),
    required=False
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
    fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

  def save(self, commit=True):
      user = super().save(commit=False)
      user.email = self.cleaned_data['username']  # Asignar el valor de username al campo email
      if commit:
          user.save()
      return user


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