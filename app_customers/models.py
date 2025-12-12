from django.db import models
from django.contrib.auth.models import User


# ---------------------------
#   CLIENTES
# ---------------------------

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Colombia")

    def __str__(self):
        return self.user.username



