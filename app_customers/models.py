from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer"
    )

    phone = models.CharField(
        max_length=20,
        help_text="Número de contacto del cliente"
    )

    department = models.CharField(
        max_length=100,
        help_text="Departamento"
    )

    city = models.CharField(
        max_length=100,
        help_text="Ciudad"
    )

    neighborhood = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Barrio"
    )

    address = models.CharField(
        max_length=255,
        help_text="Dirección principal"
    )

    note = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        help_text="Observaciones del pedido"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
