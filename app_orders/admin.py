# app_orders/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum
from decimal import Decimal

from app_orders.models import Order, OrderItem, ProviderWebhookLog, CartReservation


# ===========================
# ITEMS DE ÓRDEN (Inline)
# ===========================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal_display',)
    fields = ('product', 'variant', 'quantity', 'price', 'subtotal_display')
    
    def subtotal_display(self, obj):
        """Subtotal calculado"""
        subtotal = float(obj.quantity * obj.price)
        return format_html(
            '<span style="font-weight: bold; color: #4caf50;">${}</span>',
            f'{subtotal:,.0f}'
        )
    subtotal_display.short_description = 'Subtotal'


# ===========================
# ÓRDENES
# ===========================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'customer_info',
        'status_badge',
        'items_count',
        'total_display',
        'created_at'
    )
    
    list_filter = ('status', 'created_at', 'shipping_company')
    search_fields = (
        'id',
        'customer__user__username',
        'customer__user__first_name',
        'customer__user__last_name',
        'customer__phone',
        'tracking_number'
    )
    
    readonly_fields = (
        'created_at',
        'items_count',
        'total_items',
        'customer_detail'
    )
    
    inlines = [OrderItemInline]
    
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información de la Orden', {
            'fields': ('customer', 'customer_detail', 'status')
        }),
        ('Totales', {
            'fields': ('total', 'items_count', 'total_items')
        }),
        ('Proveedor', {
            'fields': ('provider_order_id', 'provider_response'),
            'classes': ('collapse',)
        }),
        ('Envío', {
            'fields': ('tracking_number', 'shipping_company'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = [
        'mark_as_sent_to_provider',
        'mark_as_accepted',
        'mark_as_shipped',
        'mark_as_delivered',
        'mark_as_canceled'
    ]
    
    def order_number(self, obj):
        """Número de orden destacado"""
        return format_html(
            '<span style="background: #2196F3; color: white; padding: 6px 12px; border-radius: 8px; font-weight: bold; font-family: monospace;">#{}</span>',
            str(obj.id).zfill(5)
        )
    order_number.short_description = 'N° Orden'
    
    def customer_info(self, obj):
        """Información del cliente"""
        if obj.customer:
            url = reverse('admin:app_customers_customer_change', args=[obj.customer.id])
            name = obj.customer.user.get_full_name() or obj.customer.user.username
            phone = obj.customer.phone
            
            return format_html(
                '<div style="line-height: 1.6;">'
                '<a href="{}" style="color: #2196F3; text-decoration: none; font-weight: 600;">{}</a><br>'
                '<small style="color: #666;"><i class="bi bi-phone"></i> {}</small>'
                '</div>',
                url, name, phone
            )
        return '—'
    customer_info.short_description = 'Cliente'
    
    def customer_detail(self, obj):
        """Detalle completo del cliente"""
        if obj.customer:
            return format_html(
                '<div style="padding: 10px; background: #f5f5f5; border-radius: 8px;">'
                '<p><strong>Nombre:</strong> {}</p>'
                '<p><strong>Teléfono:</strong> {}</p>'
                '<p><strong>Dirección:</strong> {}</p>'
                '<p><strong>Ciudad:</strong> {}, {}</p>'
                '</div>',
                obj.customer.user.get_full_name() or obj.customer.user.username,
                obj.customer.phone,
                obj.customer.address,
                obj.customer.city,
                obj.customer.department
            )
        return 'Sin cliente'
    customer_detail.short_description = 'Detalles del Cliente'
    
    def status_badge(self, obj):
        """Badge de estado con colores"""
        status_config = {
            'pending': ('#ff9800', '⏳ PENDIENTE'),
            'sent_to_provider': ('#2196F3', '📤 ENVIADA'),
            'accepted': ('#00bcd4', '✓ ACEPTADA'),
            'shipped': ('#9c27b0', '🚚 ENVIADO'),
            'delivered': ('#4caf50', '✓ ENTREGADO'),
            'canceled': ('#f44336', '✕ CANCELADO'),
            'error': ('#f44336', '⚠ ERROR'),
        }
        
        color, text = status_config.get(obj.status, ('#9e9e9e', obj.get_status_display()))
        
        return format_html(
            '<span style="background: {}; color: white; padding: 6px 14px; border-radius: 12px; font-size: 11px; font-weight: bold; white-space: nowrap;">{}</span>',
            color, text
        )
    status_badge.short_description = 'Estado'
    
    def items_count(self, obj):
        """Cantidad de items"""
        count = obj.items.count()
        return format_html(
            '<span style="background: #673ab7; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{} items</span>',
            count
        )
    items_count.short_description = 'Items'
    
    def total_items(self, obj):
        """Cantidad total de productos"""
        total = obj.items.aggregate(total=Sum('quantity'))['total'] or 0
        return f'{total} unidades'
    total_items.short_description = 'Total Unidades'
    
    def total_display(self, obj):
        """Total formateado"""
        total = float(obj.total)
        return format_html(
            '<span style="color: #4caf50; font-weight: bold; font-size: 16px;">${}</span>',
            f'{total:,.0f}'
        )
    total_display.short_description = 'Total'
    
    # Acciones masivas
    def mark_as_sent_to_provider(self, request, queryset):
        updated = queryset.update(status='sent_to_provider')
        self.message_user(request, f'{updated} órdenes marcadas como enviadas al proveedor.')
    mark_as_sent_to_provider.short_description = '📤 Marcar como enviada al proveedor'
    
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f'{updated} órdenes marcadas como aceptadas.')
    mark_as_accepted.short_description = '✓ Marcar como aceptada'
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} órdenes marcadas como enviadas.')
    mark_as_shipped.short_description = '🚚 Marcar como enviada'
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} órdenes marcadas como entregadas.')
    mark_as_delivered.short_description = '✓ Marcar como entregada'
    
    def mark_as_canceled(self, request, queryset):
        updated = queryset.update(status='canceled')
        self.message_user(request, f'{updated} órdenes canceladas.')
    mark_as_canceled.short_description = '✕ Cancelar órdenes'


# ===========================
# ITEMS DE ÓRDEN
# ===========================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order_link',
        'product_info',
        'variant_info',
        'quantity',
        'price_display',
        'subtotal'
    )
    
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('order__id', 'product__name', 'variant__sku')
    
    def order_link(self, obj):
        """Link a la orden"""
        url = reverse('admin:app_orders_order_change', args=[obj.order.id])
        order_number = str(obj.order.id).zfill(5)
        
        return format_html(
            '<a href="{}" style="color: #2196F3; text-decoration: none; font-weight: bold;">Orden #{}</a>',
            url, order_number
        )
    order_link.short_description = 'Orden'
    
    def product_info(self, obj):
        """Información del producto"""
        if obj.product:
            return obj.product.name
        return '—'
    product_info.short_description = 'Producto'
    
    def variant_info(self, obj):
        """Información de la variante"""
        if obj.variant:
            return format_html(
                '<span style="background: #e3f2fd; color: #1976d2; padding: 4px 8px; border-radius: 4px; font-family: monospace; font-size: 11px;">{}</span>',
                obj.variant.sku
            )
        return '—'
    variant_info.short_description = 'SKU'
    
    def price_display(self, obj):
        """Precio unitario"""
        price = float(obj.price)
        return format_html(
            '<span style="font-weight: 500;">${}</span>',
            f'{price:,.0f}'
        )
    price_display.short_description = 'Precio Unit.'
    
    def subtotal(self, obj):
        """Subtotal del item"""
        subtotal = float(obj.quantity * obj.price)
        return format_html(
            '<span style="color: #4caf50; font-weight: bold;">${}</span>',
            f'{subtotal:,.0f}'
        )
    subtotal.short_description = 'Subtotal'


# ===========================
# WEBHOOKS DEL PROVEEDOR
# ===========================

@admin.register(ProviderWebhookLog)
class ProviderWebhookLogAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'received_at', 'data_preview')
    list_filter = ('event_type', 'received_at')
    search_fields = ('event_type', 'data')
    readonly_fields = ('event_type', 'data', 'received_at', 'data_formatted')
    date_hierarchy = 'received_at'
    
    fieldsets = (
        ('Información del Webhook', {
            'fields': ('event_type', 'received_at')
        }),
        ('Datos', {
            'fields': ('data_formatted',)
        }),
    )
    
    def data_preview(self, obj):
        """Preview de los datos"""
        import json
        try:
            data_str = json.dumps(obj.data, indent=2)[:100]
            return format_html(
                '<code style="background: #f5f5f5; padding: 4px 8px; border-radius: 4px; font-size: 11px;">{}</code>',
                data_str
            )
        except:
            return '—'
    data_preview.short_description = 'Datos'
    
    def data_formatted(self, obj):
        """Datos formateados"""
        import json
        try:
            data_str = json.dumps(obj.data, indent=2)
            return format_html(
                '<pre style="background: #f5f5f5; padding: 15px; border-radius: 8px; overflow: auto; max-height: 400px;">{}</pre>',
                data_str
            )
        except:
            return 'Error al formatear'
    data_formatted.short_description = 'Datos Completos'


# ===========================
# RESERVAS DE CARRITO
# ===========================

@admin.register(CartReservation)
class CartReservationAdmin(admin.ModelAdmin):
    list_display = (
        'session_key',
        'variant',
        'quantity',
        'status_badge',
        'created_at',
        'expires_at'
    )
    
    list_filter = ('is_active', 'created_at', 'expires_at')
    search_fields = ('session_key', 'variant__sku')
    readonly_fields = ('created_at', 'expires_at')
    
    actions = ['mark_as_inactive', 'clean_expired_reservations']
    
    def status_badge(self, obj):
        """Estado de la reserva"""
        from django.utils import timezone
        
        if not obj.is_active:
            return format_html(
                '<span style="background: #9e9e9e; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">✕ INACTIVA</span>'
            )
        elif obj.expires_at < timezone.now():
            return format_html(
                '<span style="background: #f44336; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">⏰ EXPIRADA</span>'
            )
        else:
            return format_html(
                '<span style="background: #4caf50; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">✓ ACTIVA</span>'
            )
    status_badge.short_description = 'Estado'
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} reservas marcadas como inactivas.')
    mark_as_inactive.short_description = '✕ Marcar como inactivas'
    
    def clean_expired_reservations(self, request, queryset):
        count = CartReservation.clean_expired()
        self.message_user(request, f'{count} reservas expiradas limpiadas.')
    clean_expired_reservations.short_description = '🧹 Limpiar reservas expiradas'