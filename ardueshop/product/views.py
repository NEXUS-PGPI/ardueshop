from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# Create your views here.
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    quantity_range = range(1, 11)  # This generates numbers from 1 to 10

    return render(request, 'product/detail.html', {'product': product, 'quantity_range': quantity_range})
def catalogue(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'product/product_list.html', {'products': products, 'categories': categories})



