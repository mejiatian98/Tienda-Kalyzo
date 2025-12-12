from django.db import models
from app_products.models import Product, ProductVariant
from app_customers.models import Customer

# ---------------------------
#   ÓRDENES
# ---------------------------

class Order(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pendiente"),
        ("sent_to_provider", "Enviada al proveedor"),
        ("accepted", "Proveedor aceptó la orden"),
        ("shipped", "Enviado"),
        ("delivered", "Entregado"),
        ("canceled", "Cancelado"),
        ("error", "Error con proveedor"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")

    # Relación con el proveedor
    provider_order_id = models.CharField(max_length=200, blank=True, null=True)
    provider_response = models.JSONField(blank=True, null=True)

    # Tracking
    tracking_number = models.CharField(max_length=200, blank=True, null=True)
    shipping_company = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # precio de venta

    provider_product_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Item de orden {self.order.id}"



# ---------------------------
#   WEBHOOKS DEL PROVEEDOR
# ---------------------------

class ProviderWebhookLog(models.Model):
    event_type = models.CharField(max_length=100)
    data = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Webhook {self.event_type} - {self.received_at}"
