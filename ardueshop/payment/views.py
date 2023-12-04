from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from order.models import Order
from authentication.models import ArduUser
from .forms import SaveDataForm


# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get("order_id", None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
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

        # add order items to the Stripe checkout session
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

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)

        # redirect to Stripe payment form
        return redirect(session.url, code=303)

    else:
        return render(request, "payment/process.html", locals())


def payment_completed(request):
    form = SaveDataForm()
    if request.method == "POST":
        form = SaveDataForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            ardu_user = ArduUser.objects.get(user=user)
            order = Order.objects.get(id=request.session.get("order_id"))
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

    return render(request, "payment/completed.html", {"form": form})


def payment_canceled(request):
    return render(request, "payment/canceled.html")
