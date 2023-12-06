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

    PAYMENT_METHOD_CHOICES = (
        ("Tarjeta", "Tarjeta"),
        ("Contra-reembolso", "Contra-reembolso"),
    )

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def get_order_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_shipping_cost(self):
        if self.get_order_cost() >= 50:
            return 0
        else:
            return 5

    def get_total_cost(self):
        return self.get_order_cost() + self.get_shipping_cost()


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
    CLAIM_STATUS_CHOICES = (
        ("Pendiente", "Pendiente"),
        ("Atendida", "Atendida"),
    )

    claim_status = models.CharField(
        max_length=20, choices=CLAIM_STATUS_CHOICES, default="Pendiente"
    )

    response = models.TextField()

    def __str__(self):
        return f"Reclamacion #{self.id} - {self.order.email}"
    
    class Meta:
        ordering = ["-creation_date"]
        indexes = [
            models.Index(fields=["-creation_date"]),
        ]
