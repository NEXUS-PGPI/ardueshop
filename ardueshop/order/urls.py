from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path('<int:id>/', views.order_status, name='order_status'),
]
