from django.contrib import admin

# ===========================
# IMPORTS
# ===========================

from app_orders.models import (Product,ProductVariant)
from app_products.models import (Category, Option, OptionValue,
                                 ProductVariantImage, VariantOption, CommentPublic)
from app_orders.models import (Order, OrderItem, ProviderWebhookLog)



from app_customers.models import Customer


# ===========================
# CATEGORÍAS
# ===========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


# ===========================
# PRODUCTOS
# ===========================

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "is_active",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "category",
        "is_active",
        "is_featured",
    )

    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductVariantInline]


# ===========================
# OPCIONES (Color, Talla, etc.)
# ===========================

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(OptionValue)
class OptionValueAdmin(admin.ModelAdmin):
    list_display = ("option", "value", "hex_color", "order")
    list_filter = ("option",)
    ordering = ("option", "order")


# ===========================
# VARIANTES
# ===========================

class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage
    extra = 1


class VariantOptionInline(admin.TabularInline):
    model = VariantOption
    extra = 1


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "product",
        "price",
        "discount_price",
        "stock",
        "is_active",
    )

    list_filter = ("is_active", "product")
    search_fields = ("sku", "product__name")

    inlines = [
        ProductVariantImageInline,
        VariantOptionInline,
    ]


# ===========================
# IMÁGENES DE VARIANTES
# ===========================

@admin.register(ProductVariantImage)
class ProductVariantImageAdmin(admin.ModelAdmin):
    list_display = ("variant", "is_main")
    list_filter = ("is_main",)


# ===========================
# COMENTARIOS
# ===========================

@admin.register(CommentPublic)
class CommentPublicAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("name", "comment")


# ===========================
# CLIENTES
# ===========================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "city", "country")
    search_fields = ("user__username", "phone")


# ===========================
# ÓRDENES
# ===========================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "status",
        "total",
        "created_at",
    )

    list_filter = ("status", "created_at")
    search_fields = ("id", "customer__user__username")
    inlines = [OrderItemInline]


# ===========================
# ITEMS DE ÓRDEN
# ===========================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "variant",
        "quantity",
        "price",
    )


# ===========================
# WEBHOOKS DEL PROVEEDOR
# ===========================

@admin.register(ProviderWebhookLog)
class ProviderWebhookLogAdmin(admin.ModelAdmin):
    list_display = ("event_type", "received_at")
    list_filter = ("event_type",)
