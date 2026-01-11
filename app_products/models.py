from django.db import models
from django.db.models import Avg

# ---------------------------
#   CATEGORÍAS
# ---------------------------
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Nombre de la categoría
    slug = models.SlugField(unique=True)  # Slug para URL
    description = models.TextField(blank=True)  # Descripción opcional
    imagen_category = models.ImageField(upload_to="categories/", blank=True, null=True)  # Imagen de la categoría, se guarde en aws s3 bucket


    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name



# ---------------------------
#   PRODUCTOS
# ---------------------------

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )  # Categoría del producto

    name = models.CharField(max_length=200)  # Nombre del producto
    slug = models.SlugField(unique=True)  # URL amigable
    description_short = models.TextField(blank=True)  # Descripción corta
    description_long = models.TextField(blank=True)  # Descripción larga
    warranty = models.TextField(blank=True)  # Garantia
    
    sales_count = models.IntegerField(default=0)  # Ranking de ventas
    is_active = models.BooleanField(default=True, choices=((True, "Activo"), (False, "Inactivo")),)  # Producto activo
    is_featured = models.BooleanField(default=False)  # Producto destacado
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha creación

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_featured"]),
        ]

    def __str__(self):
        return self.name
    

    @property
    def avg_rating(self):
        avg = self.comments.aggregate(avg=Avg("rating"))["avg"]
        return round(avg) if avg else 0

        


    

# ---------------------------
#   VARIANTES DE PRODUCTOS
# ---------------------------
class Option(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        choices=[
            ("Color", "Color"),
            ("Medida", "Medida"),
            ("Peso", "Peso"),
            ("Material", "Material"),
        ]
    )

    def __str__(self):
        return self.name


    

# ----------------------------
#  OPCIONES Y VALORES DE PRODUCTOS
# ----------------------------

class OptionValue(models.Model):
    option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        related_name="values"
    )  # Opción padre

    value = models.CharField(max_length=50)  # Valor visible
    order = models.PositiveIntegerField(default=0)  # Orden visual

    class Meta:
        unique_together = ("option", "value")
        ordering = ["order"]

    def __str__(self):
        return f"{self.option.name}: {self.value}"


    


# ---------------------------
#   VARIANTES DE PRODUCTOS
# ---------------------------



class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    provider_variant_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sku"]

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()

    @property
    def discount_percentage(self):
        if self.discount_price and self.price:
            return round((self.price - self.discount_price) / self.price * 100)
        return 0

    @property
    def stock_status(self):
        if self.stock <= 0:
            return {"label": "Agotado", "available": False}
        if self.stock <= 5:
            return {"label": f"Últimas {self.stock}", "available": True}
        return {"label": f"{self.stock} disponibles", "available": True}

    


# ---------------------------
#   IMÁGENES DE VARIANTES
# ---------------------------

class ProductVariantImage(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        related_name="images",
        on_delete=models.CASCADE
    )  # Variante asociada

    image_url = models.URLField()  # URL de imagen
    alt_text = models.CharField(max_length=200, blank=True)  # SEO / accesibilidad
    is_main = models.BooleanField(default=False)  # Imagen principal

    class Meta:
        ordering = ["-is_main"]

    def __str__(self):
        return f"Imagen de {self.variant.sku}"
    
    @property
    def main_image(self):
        return self.images.order_by("-is_main").first()



# ---------------------------
#   OPCIONES DE VARIANTES
# ---------------------------
class VariantOption(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="options"
    )  # Variante

    option_value = models.ForeignKey(
        OptionValue,
        on_delete=models.CASCADE,
        related_name="variant_values"
    )  # Valor (Rojo, M)

    class Meta:
        unique_together = ("variant", "option_value")

    def __str__(self):
        return f"{self.variant.sku} → {self.option_value}"




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
        choices=[(i, i) for i in range(1, 6)]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating}★ - {self.name}"

