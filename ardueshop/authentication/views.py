from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import ClientCreationForm, ClientLoginForm
from django.contrib.auth import login, logout
from .backends import EmailBackend

# Create your views here.

def signup_view(request):
  if request.method == 'POST':
      form = ClientCreationForm(request.POST)
      if form.is_valid():
          # save user to database
          form.save()
          # log user in
          email = form.cleaned_data.get('email')
          password = form.cleaned_data.get('password1')
          user = EmailBackend().authenticate(request=request,username=email, password=password)
          login(request, user)
          return redirect('home')
  else:
      form = ClientCreationForm()
  return render(request, 'authentication/signup.html', {'form': form})

def login_view(request):
  if request.method == 'POST':
      form = ClientLoginForm(request.POST)
      if form.is_valid():
          # log user in
          user = EmailBackend().authenticate(request=request,username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
          login(request, user)
          return redirect('home')
  else:
      form = ClientLoginForm()
  return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
  logout(request)
  return redirect('home')