from django.contrib import admin
from django.urls import path
from claim import views as claim_views
from authentication import views as authentication_views

urlpatterns = [
  path('do_claim/', claim_views.do_claim, name='do_claim'),
  path('auth/login/', authentication_views.login_view, name='login'),
  path('auth/signup/', authentication_views.signup_view, name='register'),
  # path('my_claims/', claim_views.my_claims, name='my_claims'),
]
