from django.db import models

# ---------------------------
#   CATEGORÍAS
# ---------------------------
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



# ---------------------------
#   PRODUCTOS
# ---------------------------

class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product', 
        related_name='images',
        on_delete=models.CASCADE
    )
    image_url = models.URLField()
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Imagen de {self.product.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sales_count = models.IntegerField(default=0)

    provider_id = models.CharField(max_length=100, blank=True, null=True)
    provider_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=100)        # Ej: Color
    value = models.CharField(max_length=100)       # Ej: Rojo
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    provider_variant_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"



