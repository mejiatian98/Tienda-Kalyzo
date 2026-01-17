# app_products/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum, Avg
from django.urls import reverse
from django.utils.safestring import mark_safe

from app_products.models import (
    Category,
    Product,
    ProductVariant,
    ProductVariantImage,
    Option,
    OptionValue,
    VariantOption,
    CommentPublic
)


# ===========================
# CATEGORÍAS
# ===========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview_image', 'product_count', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('preview_image_large',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Imagen', {
            'fields': ('imagen_category', 'preview_image_large')
        }),
    )
    
    def preview_image(self, obj):
        """Miniatura de la categoría en el listado"""
        if obj.imagen_category:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.imagen_category.url
            )
        return '—'
    preview_image.short_description = 'Imagen'
    
    def preview_image_large(self, obj):
        """Vista previa grande en el detalle"""
        if obj.imagen_category:
            return format_html(
                '<img src="{}" width="300" style="border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.imagen_category.url
            )
        return 'Sin imagen'
    preview_image_large.short_description = 'Vista Previa'
    
    def product_count(self, obj):
        """Contador de productos en la categoría"""
        count = obj.products.count()
        return format_html(
            '<span style="background: #2196F3; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px;">{} productos</span>',
            count
        )
    product_count.short_description = 'Productos'


# ===========================
# PRODUCTOS
# ===========================

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    show_change_link = True
    fields = ('sku', 'price', 'discount_price', 'stock', 'is_active', 'preview_stock')
    readonly_fields = ('preview_stock',)
    
    def preview_stock(self, obj):
        """Indicador visual de stock"""
        if obj.stock <= 0:
            color = '#f44336'
            text = 'AGOTADO'
        elif obj.stock <= 5:
            color = '#ff9800'
            text = f'BAJO ({obj.stock})'
        else:
            color = '#4caf50'
            text = f'OK ({obj.stock})'
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 10px;">{}</span>',
            color, text
        )
    preview_stock.short_description = 'Estado'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'variant_count',
        'total_stock',
        'avg_rating_display',
        'sales_count',
        'status_badge',
        'featured_badge',
        'created_at'
    )
    
    list_filter = (
        'category',
        'is_active',
        'is_featured',
        'created_at',
    )
    
    search_fields = ('name', 'description_short', 'description_long', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'avg_rating_display', 'total_stock', 'variant_count')
    
    inlines = [ProductVariantInline]
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('name', 'slug', 'category')
        }),
        ('Descripciones', {
            'fields': ('description_short', 'description_long', 'warranty'),
            'classes': ('collapse',)
        }),
        ('Estado y Configuración', {
            'fields': ('is_active', 'is_featured', 'sales_count')
        }),
        ('Estadísticas', {
            'fields': ('created_at', 'avg_rating_display', 'total_stock', 'variant_count'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_products', 'deactivate_products', 'mark_as_featured', 'unmark_as_featured']
    
    def variant_count(self, obj):
        """Contador de variantes"""
        count = obj.variants.count()
        return format_html(
            '<span style="background: #9c27b0; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px;">{} variantes</span>',
            count
        )
    variant_count.short_description = 'Variantes'
    
    def total_stock(self, obj):
        """Stock total de todas las variantes"""
        total = obj.variants.aggregate(total=Sum('stock'))['total'] or 0
        
        if total <= 0:
            color = '#f44336'
        elif total <= 10:
            color = '#ff9800'
        else:
            color = '#4caf50'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} unidades</span>',
            color, total
        )
    total_stock.short_description = 'Stock Total'
    
    def avg_rating_display(self, obj):
        """Rating promedio con estrellas"""
        rating = obj.avg_rating
        stars = '★' * rating + '☆' * (5 - rating)
        comments_count = obj.comments.count()
        
        return format_html(
            '<span style="color: #ffc107; font-size: 16px;" title="{} comentarios">{}</span> <small>({} comentarios)</small>',
            comments_count, stars, comments_count
        )
    avg_rating_display.short_description = 'Rating'
    
    def status_badge(self, obj):
        """Badge de estado activo/inactivo"""
        if obj.is_active:
            return format_html(
                '<span style="background: #4caf50; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">✓ ACTIVO</span>'
            )
        return format_html(
            '<span style="background: #9e9e9e; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">✕ INACTIVO</span>'
        )
    status_badge.short_description = 'Estado'
    
    def featured_badge(self, obj):
        """Badge de producto destacado"""
        if obj.is_featured:
            return format_html(
                '<span style="background: #ff9800; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">⭐ DESTACADO</span>'
            )
        return '—'
    featured_badge.short_description = 'Destacado'
    
    # Acciones masivas
    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} productos activados.')
    activate_products.short_description = '✓ Activar productos seleccionados'
    
    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} productos desactivados.')
    deactivate_products.short_description = '✕ Desactivar productos seleccionados'
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} productos marcados como destacados.')
    mark_as_featured.short_description = '⭐ Marcar como destacados'
    
    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} productos desmarcados como destacados.')
    unmark_as_featured.short_description = '☆ Desmarcar como destacados'


# ===========================
# OPCIONES
# ===========================

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'values_count')
    search_fields = ('name',)
    
    def values_count(self, obj):
        """Contador de valores"""
        count = obj.values.count()
        return format_html(
            '<span style="background: #00bcd4; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px;">{} valores</span>',
            count
        )
    values_count.short_description = 'Valores'


@admin.register(OptionValue)
class OptionValueAdmin(admin.ModelAdmin):
    list_display = ('option', 'value', 'order', 'usage_count')
    list_filter = ('option',)
    list_editable = ('order',)
    ordering = ('option', 'order')
    search_fields = ('value',)
    
    def usage_count(self, obj):
        """Cuántas variantes usan este valor"""
        count = obj.variant_values.count()
        return format_html(
            '<span style="background: #673ab7; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px;">{} variantes</span>',
            count
        )
    usage_count.short_description = 'Uso'


# ===========================
# VARIANTES
# ===========================

class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage
    extra = 0
    fields = ('image_preview', 'image_url', 'alt_text', 'is_main')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        """Vista previa de la imagen"""
        if obj.image_url:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px; border: 2px solid #ddd;" />',
                obj.image_url
            )
        return 'Sin imagen'
    image_preview.short_description = 'Preview'


class VariantOptionInline(admin.TabularInline):
    model = VariantOption
    extra = 0
    autocomplete_fields = ['option_value']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'product_link',
        'price_display',
        'stock_badge',
        'status_badge',
        'created_at'
    )
    
    list_filter = ('is_active', 'product__category', 'created_at')
    search_fields = ('sku', 'product__name', 'provider_variant_id')
    readonly_fields = ('created_at', 'discount_percentage_display', 'stock_status_display')
    
    inlines = [ProductVariantImageInline, VariantOptionInline]
    
    fieldsets = (
        ('Producto', {
            'fields': ('product',)
        }),
        ('Identificación', {
            'fields': ('sku', 'provider_variant_id')
        }),
        ('Precios', {
            'fields': ('price', 'discount_price', 'discount_percentage_display')
        }),
        ('Inventario', {
            'fields': ('stock', 'stock_status_display', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_variants', 'deactivate_variants', 'set_out_of_stock']
    
    def product_link(self, obj):
        """Link al producto padre"""
        url = reverse('admin:app_products_product_change', args=[obj.product.id])
        return format_html(
            '<a href="{}" style="color: #2196F3; text-decoration: none; font-weight: 500;">{}</a>',
            url, obj.product.name
        )
    product_link.short_description = 'Producto'
    
    def price_display(self, obj):
        """Precio con descuento"""
        price = float(obj.price)
        
        if obj.discount_price:
            discount_price = float(obj.discount_price)
            discount_percentage = obj.discount_percentage
            
            return format_html(
                '<div style="line-height: 1.6;">'
                '<span style="text-decoration: line-through; color: #999; font-size: 11px;">${}</span><br>'
                '<span style="color: #f44336; font-weight: bold; font-size: 14px;">${}</span> '
                '<span style="background: #f44336; color: white; padding: 2px 6px; border-radius: 8px; font-size: 10px; font-weight: bold;">-{}%</span>'
                '</div>',
                f'{price:,.0f}',
                f'{discount_price:,.0f}',
                discount_percentage
            )
        
        return format_html(
            '<span style="font-weight: bold; font-size: 14px;">${}</span>',
            f'{price:,.0f}'
        )
    price_display.short_description = 'Precio'
    
    def stock_badge(self, obj):
        """Badge de stock con colores"""
        status = obj.stock_status
        
        if not status['available']:
            color = '#f44336'
        elif obj.stock <= 5:
            color = '#ff9800'
        else:
            color = '#4caf50'
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, status['label']
        )
    stock_badge.short_description = 'Stock'
    
    def status_badge(self, obj):
        """Badge de estado"""
        if obj.is_active:
            return format_html(
                '<span style="background: #4caf50; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">✓ ACTIVO</span>'
            )
        return format_html(
            '<span style="background: #9e9e9e; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">✕ INACTIVO</span>'
        )
    status_badge.short_description = 'Estado'
    
    def discount_percentage_display(self, obj):
        """Porcentaje de descuento calculado"""
        if obj.discount_percentage:
            return f'{obj.discount_percentage}%'
        return '—'
    discount_percentage_display.short_description = 'Descuento'
    
    def stock_status_display(self, obj):
        """Estado del stock legible"""
        return obj.stock_status['label']
    stock_status_display.short_description = 'Estado Stock'
    
    # Acciones masivas
    def activate_variants(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} variantes activadas.')
    activate_variants.short_description = '✓ Activar variantes'
    
    def deactivate_variants(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} variantes desactivadas.')
    deactivate_variants.short_description = '✕ Desactivar variantes'
    
    def set_out_of_stock(self, request, queryset):
        updated = queryset.update(stock=0)
        self.message_user(request, f'{updated} variantes marcadas sin stock.')
    set_out_of_stock.short_description = '📦 Marcar sin stock'


# ===========================
# IMÁGENES DE VARIANTES
# ===========================

@admin.register(ProductVariantImage)
class ProductVariantImageAdmin(admin.ModelAdmin):
    list_display = ('variant', 'image_preview', 'is_main', 'alt_text')
    list_filter = ('is_main',)
    search_fields = ('variant__sku', 'alt_text')
    list_editable = ('is_main',)
    
    def image_preview(self, obj):
        """Vista previa de la imagen"""
        if obj.image_url:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image_url
            )
        return 'Sin imagen'
    image_preview.short_description = 'Imagen'


# ===========================
# COMENTARIOS
# ===========================

@admin.register(CommentPublic)
class CommentPublicAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating_stars', 'comment_preview', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'comment', 'product__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Comentario', {
            'fields': ('product', 'name', 'rating', 'comment')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def rating_stars(self, obj):
        """Rating con estrellas visuales"""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        colors = {
            5: '#4caf50',
            4: '#8bc34a',
            3: '#ff9800',
            2: '#ff5722',
            1: '#f44336'
        }
        color = colors.get(obj.rating, '#999')
        
        return format_html(
            '<span style="color: {}; font-size: 18px;">{}</span>',
            color, stars
        )
    rating_stars.short_description = 'Rating'
    
    def comment_preview(self, obj):
        """Preview del comentario"""
        preview = obj.comment[:60] + '...' if len(obj.comment) > 60 else obj.comment
        return format_html(
            '<span style="color: #666; font-style: italic;">"{}"</span>',
            preview
        )
    comment_preview.short_description = 'Comentario'