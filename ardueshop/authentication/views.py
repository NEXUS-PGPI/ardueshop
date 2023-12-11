from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import ClientCreationForm, ClientLoginForm
from .models import ArduUser

# Create your views here.

def signup_view(request):
  if request.method == 'POST':
      form = ClientCreationForm(request.POST)
      if form.is_valid():
          # save user to database
          form.cleaned_data['email'] = form.cleaned_data.get('username')
          user = form.save()
          ArduUser(user=user).save()
          # log user in
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password1')
          user = authenticate(request=request,username=username, password=password)
          login(request, user)
          return redirect('home')
  else:
      form = ClientCreationForm()
  return render(request, 'authentication/signup.html', {'form': form})

def login_view(request):
  if request.method == 'POST':
      form = ClientLoginForm(request=request, data=request.POST)
      if form.is_valid():
          # log user in
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password')
          user = authenticate(request=request,username=username, password=password)
          login(request, user)
          return redirect('home')
  else:
      form = ClientLoginForm()
  return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
  logout(request)
  return redirect('home')
