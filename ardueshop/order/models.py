from django.db import models

from django.db import models
from product.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    SHIPPING_STATUS_CHOICES = (
        ("Pendiente", "Pendiente"),
        ("Enviado", "Enviado"),
        ("Entregado", "Entregado"),
    )

    shipping_status = models.CharField(
        max_length=20, choices=SHIPPING_STATUS_CHOICES, default="Pendiente"
    )

    SHIPPING_METHOD_CHOICES = (
        ("Entrega estándar", "Entrega estándar"),
        ("Recogida en tienda", "Recogida en tienda")
    )
    shipping_method = models.CharField(
        max_length=25, choices=SHIPPING_METHOD_CHOICES, default="Entrega estándar"
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def get_total_cost(self):
        cost_no_shipping = sum(item.get_cost() for item in self.items.all())
        if cost_no_shipping < 50 and self.shipping_method == "Entrega estándar":
            return cost_no_shipping + 5
        else:
            return cost_no_shipping  
            

    def get_shipping_cost(self):
        return 5


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity


class Claim(models.Model):
    order = models.ForeignKey(Order, related_name="order", on_delete=models.CASCADE)
    comment = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reclamacion #{self.id} - {self.order.email}"
