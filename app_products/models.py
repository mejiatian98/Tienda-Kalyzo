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

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    sales_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True,choices=((True, "Sí"), (False, "No")),)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True,choices=((True, "Sí"), (False, "No")),)

    # atributos
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)

    provider_variant_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.color or ''} {self.size or ''}"


class ProductVariantImage(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        related_name="images",
        on_delete=models.CASCADE
    )
    image_url = models.URLField()
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Imagen de {self.variant}"
    
    @property
    def main_image(self):
        return self.images.first()


# ---------------------------
#   COMENTARIOS
# ---------------------------

class CommentPublic(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="comments",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=5
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}★ - {self.name} en {self.product.name}"
