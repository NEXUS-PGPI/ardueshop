from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

# Create your views here.

def hello_world(request):
    return HttpResponse('<h1>Hello World</h1>')

def signup_view(request):
  if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
          # save user to database
          form.save()
          # log user in
          return redirect('')
  else:
      form = UserCreationForm()
  return render(request, 'signup.html', {'form': form})

def login_view(request):
  if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)
      if form.is_valid():
          # log user in
          return redirect('home')
  else:
      form = AuthenticationForm()
  return render(request, 'login.html', {'form': form})

def logout_view(request):
  return redirect('home')

def change_password_view(request):
  if request.method == 'POST':
      form = PasswordChangeForm(data=request.POST)
      if form.is_valid():
          # change password
          return redirect('home')
  else:
      form = PasswordChangeForm(user=request.user)
  return render(request, 'change_password.html', {'form': form})
