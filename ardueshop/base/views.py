from django.shortcuts import render
from product.models import Category


def home(request):
    categories = Category.objects.all()
    return render(request, "base/home.html", {"categories": categories})

def about(request):
    return render(request, "base/about.html")
