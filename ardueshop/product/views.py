from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# Create your views here.
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product/detail.html', {'product': product})
def catalogue(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'product/product_list.html', {'products': products, 'categories': categories})



