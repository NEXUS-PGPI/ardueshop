
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models importClaim, OrderItem, Order
from .forms import  EmailPickerForm, OrderCreateForm, ClaimForm
from datetime import timezone
from cart.cart import Cart

def my_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(email=request.user.email)
        for order in orders:
            order.claims = Claim.objects.filter(order=order)
        return render(request, 'order/my_orders.html', {'orders': orders})
    else:
        return render(request, 'order/not_authenticated_user.html')

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

def new_claim(request, order_id):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            # claim.creation_date = timezone.now()
            claim.order = Order.objects.get(id=order_id)
            claim.save()
            return redirect('order:claim', claim_id=claim.id)
    else:
        form = ClaimForm()
    
    return render(request, 'order/new_claim.html', {'form': form})

def claim(request, claim_id):
    claim = Claim.objects.get(id=claim_id)
    return render(request, 'order/claim.html', {'claim': claim})
