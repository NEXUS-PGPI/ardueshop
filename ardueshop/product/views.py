from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    quantity_range = range(1, 11)  # This generates numbers from 1 to 10
    return render(
        request,
        "product/detail.html",
        {"product": product, "quantity_range": quantity_range},
    )


def catalogue(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(
        request,
        "product/product_list.html",
        {"products": products, "categories": categories},
    )


def search_products(request):
    product_name = request.GET.get("product_name", "")
    product_category = request.GET.get("product_category", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")

    products = Product.objects.all()
    categories = Category.objects.all()

    if product_name:
        products = products.filter(name__icontains=product_name)
    if product_category:
        products = products.filter(category__name__icontains=product_category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(
        request,
        "product/product_list.html",
        {
            "products": products,
            "categories": categories,
            "product_name": product_name,
            "product_category": product_category,
            "min_price": min_price,
            "max_price": max_price,
            "search": "True",
        },
    )
