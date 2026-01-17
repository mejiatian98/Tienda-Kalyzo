# app_customers/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.urls import reverse

from app_customers.models import Customer


# ===========================
# CLIENTES
# ===========================



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'user_info',
        'phone',
        'location',
        'orders_count',
        'created_at',
        'updated_at'
    )
    
    list_filter = ('department', 'city', 'created_at')
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'phone',
        'department',
        'city',
        'address'
    )
    
    readonly_fields = ('created_at', 'updated_at', 'orders_count', 'total_spent')
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información de Contacto', {
            'fields': ('phone',)
        }),
        ('Dirección', {
            'fields': ('department', 'city', 'neighborhood', 'address')
        }),
        ('Notas', {
            'fields': ('note',),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': ('created_at', 'updated_at', 'orders_count', 'total_spent'),
            'classes': ('collapse',)
        }),
    )
    
    def user_info(self, obj):
        """Información del usuario con link"""
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        full_name = obj.user.get_full_name() or obj.user.username
        email = obj.user.email or '—'
        
        return format_html(
            '<div style="line-height: 1.6;">'
            '<a href="{}" style="color: #2196F3; text-decoration: none; font-weight: 600; font-size: 13px;">{}</a><br>'
            '<small style="color: #666;"><i class="bi bi-envelope"></i> {}</small>'
            '</div>',
            url, full_name, email
        )
    user_info.short_description = 'Cliente'
    
    def location(self, obj):
        """Ubicación completa"""
        parts = []
        if obj.neighborhood:
            parts.append(obj.neighborhood)
        parts.append(obj.city)
        parts.append(obj.department)
        
        location_str = ', '.join(parts)
        
        return format_html(
            '<div style="line-height: 1.6;">'
            '<i class="bi bi-geo-alt-fill" style="color: #f44336;"></i> '
            '<span style="font-size: 12px;">{}</span><br>'
            '<small style="color: #666;">{}</small>'
            '</div>',
            location_str, obj.address
        )
    location.short_description = 'Ubicación'
    
    def orders_count(self, obj):
        """Contador de órdenes"""
        try:
            count = obj.order_set.count()
            
            if count == 0:
                color = '#9e9e9e'
                text = 'Sin órdenes'
            elif count <= 3:
                color = '#2196F3'
                text = f'{count} órdenes'
            else:
                color = '#4caf50'
                text = f'{count} órdenes'
            
            return format_html(
                '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
                color, text
            )
        except:
            return '—'
    orders_count.short_description = 'Órdenes'
    
    def total_spent(self, obj):
        """Total gastado por el cliente"""
        try:
            from django.db.models import Sum
            total = obj.order_set.aggregate(total=Sum('total'))['total'] or 0
            
            return format_html(
                '<span style="color: #4caf50; font-weight: bold; font-size: 14px;">${:,.0f}</span>',
                total
            )
        except:
            return '$0'
    total_spent.short_description = 'Total Gastado'