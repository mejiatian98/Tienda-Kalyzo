from django.contrib import admin
from app_products.models import Product, ProductVariant, Category, ProductImage



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # cuántos inputs vacíos muestra por defecto

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
