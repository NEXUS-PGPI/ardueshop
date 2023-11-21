from django.shortcuts import render, get_object_or_404
from .models import Product
# Create your views here.
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request,
                  'product/detail.html',
                  {'product': product})