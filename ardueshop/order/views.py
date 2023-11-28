from django.shortcuts import render
from .models import OrderItem
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
            # Clear the cart
            cart.clear()
            return render(request, "base/home.html")
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
