from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Opinion
from .forms import OpinionForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def publish_opinion(request, id):
    message = None

    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            current_user = request.user
            product = get_object_or_404(Product, id=id)
            opinion = Opinion(user=current_user, product=product, comment=form.cleaned_data['comment'])
            opinion.save()            
            return redirect('product:product_detail', id=id)            

    return redirect('product:product_detail', id=id)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    quantity_range = range(1, 11)

    opinions = product.opinions.order_by('-date')
    
    return render(request, 'product/detail.html', {'product': product, 'quantity_range': quantity_range, 'opinions': opinions} )

def catalogue(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'product/product_list.html', {'products': products, 'categories': categories})
