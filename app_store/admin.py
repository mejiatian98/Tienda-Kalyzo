from django.contrib import admin
from app_products.models import Category, Product, ProductVariant, ProductVariantImage, CommentPublic

# =========================
#   CATEGORÍAS
# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


# =========================
#   IMÁGENES DE VARIANTE
# =========================
class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage
    extra = 1


# =========================
#   VARIANTES
# =========================
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True
    fields = (
        "sku",
        "color",
        "size",
        "price",
        "discount_price",
        "stock",
        "is_active",
    )


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "sku",
        "color",
        "size",
        "price",
        "discount_price",
        "stock",
        "is_active",
    )
    list_filter = ("is_active", "product")
    search_fields = ("sku", "product__name")
    inlines = [ProductVariantImageInline]


# =========================
#   PRODUCTOS
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "category")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductVariantInline]


# =========================
#   COMENTARIOS
# =========================
@admin.register(CommentPublic)
class CommentPublicAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "name",
        "rating",
        "created_at",
    )
    list_filter = ("rating", "created_at")
    search_fields = ("name", "comment", "product__name")
    readonly_fields = ("created_at",)
