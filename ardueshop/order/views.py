from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
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
            form = OrderCreateForm(
                initial={
                    "email": request.user.username,
                }
            )
        else:
            form = OrderCreateForm()
    return render(request, "order/create.html", {"form": form, "cart": cart})


def order_status(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, "order/order_status.html", {"order": order})
