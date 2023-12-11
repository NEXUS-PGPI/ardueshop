from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from order.models import Order
from authentication.models import ArduUser
from .forms import SaveDataForm


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
    # Delete the order
    order = Order.objects.get(id=request.session.get("order_id"))
    order.delete()
    return render(request, "payment/canceled.html")
