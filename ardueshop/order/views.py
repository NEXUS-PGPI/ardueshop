from datetime import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from .models import Claim, OrderItem, Order
from .forms import OrderCreateForm, ClaimForm
from cart.cart import Cart
from authentication.models import ArduUser
import stripe

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def my_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(email=request.user.email)
        for order in orders:
            order.claims = Claim.objects.filter(order=order)
        return render(request, "order/my_orders.html", {"orders": orders})
    else:
        return render(request, "order/not_authenticated_user.html")


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

            return payment_process(request, order)

    else:
        no_stock_products = []
        for item in cart:
            if item["quantity"] > item["product"].stock:
                no_stock_products.append(item["product"])
        if len(no_stock_products) > 0:
            messages.error(
                request,
                "No hay suficiente stock de los siguientes productos: {}".format(
                    ", ".join([str(p) for p in no_stock_products])
                ),
            )
            return redirect(reverse("cart:cart_detail"))

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


def new_claim(request, order_id):
    if request.method == "POST":
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            # claim.creation_date = timezone.now()
            claim.order = Order.objects.get(id=order_id)
            claim.save()
            return redirect("order:claim", claim_id=claim.id)
    else:
        form = ClaimForm()

    return render(request, "order/new_claim.html", {"form": form})


def claim(request, claim_id):
    claim = Claim.objects.get(id=claim_id)
    return render(request, "order/claim.html", {"claim": claim})


# Auxiliar functions:


def payment_process(request, order):
    success_url = request.build_absolute_uri(reverse("payment:completed"))
    cancel_url = request.build_absolute_uri(reverse("payment:canceled"))

    # Stripe checkout session data
    session_data = {
        "mode": "payment",
        "client_reference_id": order.id,
        "success_url": success_url,
        "cancel_url": cancel_url,
        "line_items": [],
    }

    # Add order items to the Stripe checkout session
    for item in order.items.all():
        session_data["line_items"].append(
            {
                "price_data": {
                    "unit_amount": int(item.price * Decimal("100")),
                    "currency": "eur",
                    "product_data": {
                        "name": item.product.name,
                    },
                },
                "quantity": item.quantity,
            }
        )

    # Create Stripe checkout session
    session = stripe.checkout.Session.create(**session_data)

    # redirect to Stripe payment form
    return redirect(session.url, code=303)
