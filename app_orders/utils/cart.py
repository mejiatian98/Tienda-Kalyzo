# app_orders/utils/cart.py

import json
import uuid
from django.utils import timezone
from datetime import timedelta
from app_orders.models import CartReservation
from app_products.models import ProductVariant

class Cart:
    """
    Clase para manejar el carrito de compras con cookies
    """
    
    def __init__(self, request):
        self.request = request
        self.session_key = self._get_or_create_session_key()
        
        # ✅ LIMPIAR RESERVAS EXPIRADAS AUTOMÁTICAMENTE
        # Esto se ejecuta cada vez que se crea una instancia del carrito
        CartReservation.clean_expired()
        
        # Cargar carrito desde cookie
        self.cart = self._load_cart()

    def _get_or_create_session_key(self):
        """Obtiene o crea una clave única para el carrito"""
        session_key = self.request.COOKIES.get('cart_session_key')
        if not session_key:
            session_key = str(uuid.uuid4())
        return session_key

    def _load_cart(self):
        """Carga el carrito desde la cookie"""
        cart_data = self.request.COOKIES.get('cart_data', '{}')
        try:
            return json.loads(cart_data)
        except json.JSONDecodeError:
            return {}

    def add(self, variant_id, quantity=1):
        """
        Agrega un producto al carrito
        Retorna: (success: bool, message: str)
        """
        try:
            variant = ProductVariant.objects.get(id=variant_id, is_active=True)
        except ProductVariant.DoesNotExist:
            return False, "Producto no encontrado"

        # Verificar stock disponible
        current_quantity = self.cart.get(str(variant_id), {}).get('quantity', 0)
        total_quantity = current_quantity + quantity

        if variant.stock < total_quantity:
            return False, f"Stock insuficiente. Disponible: {variant.stock}"

        # Actualizar o crear reserva
        reservation, created = CartReservation.objects.get_or_create(
            session_key=self.session_key,
            variant=variant,
            defaults={
                'quantity': quantity,
                'expires_at': timezone.now() + timedelta(hours=3)
            }
        )

        # ✅ SIEMPRE actualizar y guardar (sea creada o existente)
        reservation.quantity = total_quantity
        reservation.expires_at = timezone.now() + timedelta(hours=3)
        reservation.is_active = True
        reservation.save()

        # ✅ Obtener las opciones de la variante
        variant_options = []
        for vo in variant.options.all():
            variant_options.append({
                'option': vo.option_value.option.name,
                'value': vo.option_value.value
            })

        # Actualizar carrito en memoria
        if str(variant_id) in self.cart:
            self.cart[str(variant_id)]['quantity'] = total_quantity
            # ✅ Actualizar stock también cuando ya existe
            self.cart[str(variant_id)]['stock'] = variant.stock
        else:
            self.cart[str(variant_id)] = {
                'variant_id': variant_id,
                'product_id': variant.product.id,
                'product_slug': variant.product.slug,
                'product_name': variant.product.name,
                'sku': variant.sku,
                'quantity': quantity,
                'price': float(variant.discount_price or variant.price),
                'original_price': float(variant.price),
                'discount_percentage': variant.discount_percentage,
                'image': variant.main_image.image_url if variant.main_image else None,
                'options': variant_options,  # ✅ OPCIONES DE LA VARIANTE
                'stock': variant.stock  # ✅ STOCK DISPONIBLE
            }

        return True, "Producto agregado al carrito"

    def update(self, variant_id, quantity):
        """
        Actualiza la cantidad de un producto en el carrito
        """
        if quantity <= 0:
            return self.remove(variant_id)

        try:
            variant = ProductVariant.objects.get(id=variant_id)
            reservation = CartReservation.objects.get(
                session_key=self.session_key,
                variant=variant,
                is_active=True
            )
        except (ProductVariant.DoesNotExist, CartReservation.DoesNotExist):
            return False, "Producto no encontrado en el carrito"

        # ✅ Solo validar stock si está AUMENTANDO la cantidad
        if quantity > reservation.quantity:
            difference = quantity - reservation.quantity
            if variant.stock < difference:
                return False, f"Stock insuficiente. Disponible: {variant.stock}"

        # Actualizar reserva
        reservation.quantity = quantity
        reservation.expires_at = timezone.now() + timedelta(hours=3)
        reservation.save()

        # Actualizar carrito en memoria
        self.cart[str(variant_id)]['quantity'] = quantity
        # ✅ Actualizar stock en el carrito
        self.cart[str(variant_id)]['stock'] = variant.stock

        return True, "Cantidad actualizada"

    def remove(self, variant_id):
        """
        Elimina un producto del carrito
        """
        try:
            variant = ProductVariant.objects.get(id=variant_id)
            reservation = CartReservation.objects.get(
                session_key=self.session_key,
                variant=variant,
                is_active=True
            )
            
            # Marcar reserva como inactiva
            reservation.is_active = False
            reservation.save()
            
            # Eliminar del carrito en memoria
            if str(variant_id) in self.cart:
                del self.cart[str(variant_id)]
            
            return True, "Producto eliminado del carrito"
        except (ProductVariant.DoesNotExist, CartReservation.DoesNotExist):
            return False, "Producto no encontrado"

    def clear(self):
        """
        Limpia todo el carrito
        """
        reservations = CartReservation.objects.filter(
            session_key=self.session_key,
            is_active=True
        )
        
        for reservation in reservations:
            reservation.is_active = False
            reservation.save()
        
        self.cart = {}
        return True, "Carrito vaciado"

    def get_total(self):
        """Calcula el total del carrito (precio final con descuentos)"""
        return sum(
            item['price'] * item['quantity'] 
            for item in self.cart.values()
        )

    def get_savings(self):
        """Calcula el ahorro total por descuentos"""
        savings = 0
        for item in self.cart.values():
            # Si hay precio original diferente al precio actual, hay descuento
            if item.get('original_price') and item['original_price'] > item['price']:
                # Ahorro por unidad * cantidad
                savings += (item['original_price'] - item['price']) * item['quantity']
        return savings

    def get_subtotal(self):
        """Calcula el subtotal SIN descuentos (precio original)"""
        subtotal = 0
        for item in self.cart.values():
            # Usar precio original si existe, sino usar precio actual
            price = item.get('original_price', item['price'])
            subtotal += price * item['quantity']
        return subtotal

    def get_items(self):
        """Retorna los items del carrito"""
        return list(self.cart.values())

    def get_count(self):
        """Retorna la cantidad total de items"""
        return sum(item['quantity'] for item in self.cart.values())

    def save_to_response(self, response):
        """
        Guarda el carrito en las cookies de la respuesta
        """
        cart_data = json.dumps(self.cart)
        
        # Cookie del carrito (3 horas)
        response.set_cookie(
            'cart_data',
            cart_data,
            max_age=3 * 60 * 60,  # 3 horas en segundos
            httponly=True,
            samesite='Lax'
        )
        
        # Cookie de la sesión
        response.set_cookie(
            'cart_session_key',
            self.session_key,
            max_age=3 * 60 * 60,
            httponly=True,
            samesite='Lax'
        )
        
        return response