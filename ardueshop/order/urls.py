from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path('<int:id>/', views.order_status, name='order_status'),
    path("<int:order_id>/claim/new_claim", views.new_claim, name="do_claim"),
    path("claim/<int:claim_id>", views.claim, name="claim"),
    path("my_orders/", views.my_orders, name="my_orders"),
    path("order_placed/", views.order_placed, name="order_placed"),
    path("all_orders/", views.all_orders, name="all_orders"),
    path("claims/", views.list_claims, name="list_claims"),
    path('order_not_found/', views.order_not_found, name='order_not_found')
]
