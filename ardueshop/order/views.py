from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from authentication.models import ArduUser


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        if request.user.is_authenticated:
            request.POST._mutable = True
            request.POST["email"] = request.user.email
            request.POST._mutable = False
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            cart.clear()

            request.session["order_id"] = order.id

            return redirect(reverse("payment:process"))
    else:
        if request.user.is_authenticated:
            ardu_user = ArduUser.objects.get(user=request.user)
            form = OrderCreateForm(
                initial={
                    "email": request.user.email,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                    "address": ardu_user.address,
                    "postal_code": ardu_user.postal_code,
                    "city": ardu_user.city,
                }
            )
        else:
            form = OrderCreateForm()
    return render(request, "order/create.html", {"form": form, "cart": cart})
