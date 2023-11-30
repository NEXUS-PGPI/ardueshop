from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path('<int:order_id>/claim/new_claim', views.new_claim, name='do_claim'),
    path('<int:order_id>/claim/<int:claim_id>', views.claim, name='claim'),
]
