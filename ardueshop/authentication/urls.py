from django.contrib import admin
from django.urls import path
from authentication import views as authentication_views

urlpatterns = [
    path('login/', authentication_views.login_view, name='login'),
    path('signup/', authentication_views.signup_view, name='signup'),
    path('logout/', authentication_views.logout_view, name='logout'),
]
