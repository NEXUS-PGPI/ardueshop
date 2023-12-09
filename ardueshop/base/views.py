from django.shortcuts import render
from product.models import Category, Product


def home(request):
    products = Product.objects.all().order_by("?")[:3]
    categories = Category.objects.all()
    return render(request, "base/home.html", {"categories": categories, "products": products})

def about(request):
    return render(request, "base/about.html")
def order_not_found(request):
    return render(request, "order/order_not_found.html")



