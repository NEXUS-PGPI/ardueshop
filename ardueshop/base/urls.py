from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path('order_not_found/', views.order_not_found, name='order_not_found')
]
