from django.shortcuts import render, redirect
from product.models import Category, Product
from order.models import Order, OrderItem
from datetime import timedelta
from django.db.models import Count, Sum
from django.utils import timezone

def home(request):
    products = Product.objects.all().order_by("?")[:3]
    categories = Category.objects.all()
    return render(request, "base/home.html", {"categories": categories, "products": products})

def about(request):
    return render(request, "base/about.html")
def order_not_found(request):
    return render(request, "order/order_not_found.html")

def sales_report(request):
    user = request.user
    if user.is_staff:
        current_date = timezone.now()

        # Calculate the start date for the last 30 days
        last_30_days_start = current_date - timedelta(days=30)

        # Query to get the number of orders from the last 30 days
        orders_last_30_days = Order.objects.filter(
            created__range=(last_30_days_start, current_date)
        )

        number_of_orders_last_30_days = orders_last_30_days.count()

        # Calculate the total price and count of orders
        total_price_last_30_days = sum(order.get_total_cost() for order in orders_last_30_days)

        if number_of_orders_last_30_days > 0:
            average_price_last_30_days = total_price_last_30_days / number_of_orders_last_30_days
        else:
            average_price_last_30_days ="Sin pedidos en los últimos 30 días"
        
        all_orders = Order.objects.all()
        total_benefits = sum(order.get_total_cost() for order in all_orders)

        preferred_shipping_last_30_days = orders_last_30_days.values('shipping_method').annotate(shipping_count=Count('shipping_method')).order_by('-shipping_count').first()

        if preferred_shipping_last_30_days:
            preferred_shipping_option = preferred_shipping_last_30_days['shipping_method']
        else:
            preferred_shipping_option = "Sin pedidos en los últimos 30 días"

        most_popular_products = OrderItem.objects.filter(
            order__created__range=(last_30_days_start, current_date)
        ).values('product__id', 'product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

        # Retrieve product details for the most popular products
        popular_products = []
        for popular_product in most_popular_products:
            product_id = popular_product['product__id']
            total_quantity = popular_product['total_quantity']
            product = Product.objects.get(id=product_id)
            popular_products.append({'product': product, 'total_quantity': total_quantity})



        return render(request, "base/sales_report.html",{
            "number_of_orders_last_30_days": number_of_orders_last_30_days,
            "average_price_last_30_days": average_price_last_30_days,
            "total_price_last_30_days": total_price_last_30_days,
            "total_benefits": total_benefits,
            "preferred_shipping_option": preferred_shipping_option,
            "popular_products": popular_products,
        })
    else:
        return redirect("/auth/login")        # Get the current date and time in the current time zone
