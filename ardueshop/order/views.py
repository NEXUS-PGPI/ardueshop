
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Claim, OrderItem, Order

from .forms import  EmailPickerForm, OrderCreateForm, ClaimForm
from datetime import timezone
from payment.forms import SaveDataForm
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

            if order.payment_method == "Tarjeta":
                return payment_process(request, order)
            else:
                order.shipping_status = "Enviado"
                order.save()
                # Update product stock
                for item in order.items.all():
                    item.product.stock -= item.quantity
                    item.product.save()
                # Send confirmation email
                order.send_confirmation_email()
                return redirect(reverse("order:order_placed"))

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

def order_status(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, "order/order_status.html", {"order": order})

def order_placed(request):
    order = Order.objects.get(id=request.session.get("order_id"))
    form = SaveDataForm()
    if request.method == "POST":
        form = SaveDataForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            ardu_user = ArduUser.objects.get(user=user)
            if form.cleaned_data["save_data_checkbox"]:
                user.first_name = order.first_name
                user.last_name = order.last_name
                user.save()
                ardu_user.address = order.address
                ardu_user.postal_code = order.postal_code
                ardu_user.city = order.city
                ardu_user.save()

            else:
                user.first_name = ""
                user.last_name = ""
                user.save()
                ardu_user.address = None
                ardu_user.postal_code = None
                ardu_user.city = None
                ardu_user.save()

            return redirect(reverse("catalogue:catalogue"))

    return render(request, "order/order_placed.html", {"order": order, "form": form})


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

    if order.get_total_cost() < 50 and order.shipping_method == "Entrega estándar":
        session_data["line_items"].append(
            {
                "price_data": {
                    "unit_amount": int(order.get_shipping_cost() * Decimal("100")),
                    "currency": "eur",
                    "product_data": {
                        "name": "Costes de envío",
                    },
                },
                "quantity": 1,
            }
        )

    # Create Stripe checkout session
    session = stripe.checkout.Session.create(**session_data)

    # Redirect to Stripe payment form
    return redirect(session.url, code=303)
