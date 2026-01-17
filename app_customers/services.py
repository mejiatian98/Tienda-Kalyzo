# app_customers/services.py
# -*- coding: utf-8 -*-

from django.db import transaction
from django.contrib.auth.models import User
from decimal import Decimal

from app_orders.models import Order, OrderItem
from app_customers.models import Customer
from app_orders.utils.cart import Cart
from app_products.models import Product  # ✅ Importar Product

class OrderService:
    """Servicio para manejar la lógica de negocio de las órdenes"""
    
    @staticmethod
    def create_order_from_cart(request, form_data):
        """
        Crea una orden a partir del carrito actual.
        
        Returns:
            tuple: (order, whatsapp_message, success, error_message)
        """
        try:
            with transaction.atomic():
                # 1. Obtener carrito
                cart = Cart(request)
                cart_items = cart.get_items()
                
                if not cart_items:
                    return None, None, False, 'El carrito está vacío'
                
                # 2. Obtener o crear usuario y customer
                user, customer = OrderService._get_or_create_user_and_customer(
                    request,
                    form_data
                )
                
                # 3. Crear orden
                order = Order()
                order.customer = customer
                order.status = 'pending'
                
                # Calcular total
                total = Decimal('0')
                for item in cart_items:
                    item_price = Decimal(str(item['price']))
                    quantity = item['quantity']
                    total += item_price * quantity
                
                order.total = total
                order.save()
                
                # 4. Crear items de la orden e incrementar sales_count
                for item in cart_items:
                    # Crear OrderItem
                    OrderItem.objects.create(
                        order=order,
                        product_id=item['product_id'],
                        variant_id=item['variant_id'],
                        quantity=item['quantity'],
                        price=Decimal(str(item['price']))
                    )
                    
                    # ✅ Incrementar sales_count del producto
                    try:
                        product = Product.objects.get(id=item['product_id'])
                        product.sales_count += item['quantity']  # Sumar la cantidad vendida
                        product.save(update_fields=['sales_count'])
                        print(f"✅ Product {product.id} sales_count actualizado a {product.sales_count}")
                    except Product.DoesNotExist:
                        print(f"⚠️ Producto {item['product_id']} no encontrado")
                
                # 5. Generar mensaje de WhatsApp
                whatsapp_message = OrderService._generate_whatsapp_message(
                    order,
                    cart_items,
                    form_data
                )
                
                # 6. ✅ NO limpiar carrito aquí - se limpiará en el frontend
                # cart.clear()
                
                return order, whatsapp_message, True, None
        
        except Exception as e:
            import traceback
            print(f"Error en create_order_from_cart: {e}")
            print(traceback.format_exc())
            return None, None, False, f'Error al crear la orden: {str(e)}'
    
    @staticmethod
    def _get_or_create_user_and_customer(request, form_data):
        """Obtiene o crea un usuario y su perfil de Customer"""
        if request.user.is_authenticated:
            user = request.user
        else:
            # Crear usuario temporal (guest)
            phone = form_data['customer_phone']
            username = f"guest_{phone}"
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': form_data['customer_name'].split()[0] if form_data['customer_name'] else '',
                    'last_name': ' '.join(form_data['customer_name'].split()[1:]) if len(form_data['customer_name'].split()) > 1 else '',
                    'email': form_data.get('customer_email', ''),
                }
            )
            
            if not created:
                # Actualizar nombre si cambió
                user.first_name = form_data['customer_name'].split()[0] if form_data['customer_name'] else ''
                user.last_name = ' '.join(form_data['customer_name'].split()[1:]) if len(form_data['customer_name'].split()) > 1 else ''
                if form_data.get('customer_email'):
                    user.email = form_data['customer_email']
                user.save()
        
        # Crear o actualizar Customer
        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={
                'phone': form_data['customer_phone'],
                'department': form_data['department'],
                'city': form_data['city'],
                'neighborhood': form_data.get('neighborhood', ''),
                'address': form_data['address'],
                'note': form_data.get('note', ''),
            }
        )
        
        if not created:
            # Actualizar con los datos más recientes
            customer.phone = form_data['customer_phone']
            customer.department = form_data['department']
            customer.city = form_data['city']
            customer.neighborhood = form_data.get('neighborhood', '')
            customer.address = form_data['address']
            customer.note = form_data.get('note', '')
            customer.save()
        
        return user, customer
    
    @staticmethod
    def _generate_whatsapp_message(order, cart_items, form_data):
        """
        Generar mensaje formateado para WhatsApp con emojis.
        Asegura encoding UTF-8 correcto.
        """
        # Construir mensaje con emojis Unicode
        mensaje = "🛒 *NUEVO PEDIDO - KALYZO SHOP*\n\n"
        mensaje += f"📋 *ORDEN #{order.id}*\n\n"
        
        mensaje += "👤 *DATOS DEL CLIENTE*\n"
        mensaje += f"Nombre: {form_data['customer_name']}\n"
        mensaje += f"📱 Teléfono: {form_data['customer_phone']}\n"
        
        if form_data.get('customer_email'):
            mensaje += f"📧 Email: {form_data['customer_email']}\n"
        
        mensaje += "\n📍 *DIRECCIÓN DE ENTREGA*\n"
        mensaje += f"Departamento: {form_data['department']}\n"
        mensaje += f"Ciudad: {form_data['city']}\n"
        
        if form_data.get('neighborhood'):
            mensaje += f"Barrio: {form_data['neighborhood']}\n"
        
        mensaje += f"Dirección: {form_data['address']}\n\n"
        
        mensaje += "📦 *PRODUCTOS*\n"
        mensaje += "━━━━━━━━━━━━━━━━\n"
        
        for index, item in enumerate(cart_items, 1):
            item_total = item['price'] * item['quantity']
            
            mensaje += f"\n{index}. *{item['product_name']}*\n"
            mensaje += f"   • SKU: {item['sku']}\n"
            mensaje += f"   • Cantidad: {item['quantity']}\n"
            
            # Opciones
            if item.get('options'):
                mensaje += "   • Opciones: "
                opts = [f"{opt['option']}: {opt['value']}" for opt in item['options']]
                mensaje += ', '.join(opts) + '\n'
            
            mensaje += f"   • Precio unitario: ${int(item['price']):,}\n"
            mensaje += f"   • Subtotal: ${int(item_total):,}\n"
        
        mensaje += "\n━━━━━━━━━━━━━━━━\n"
        mensaje += f"💰 *TOTAL A PAGAR: ${int(order.total):,}*\n\n"
        
        if form_data.get('note'):
            mensaje += "📝 *OBSERVACIONES*\n"
            mensaje += f"{form_data['note']}\n\n"
        
        mensaje += "✅ Pago contraentrega\n"
        mensaje += "🚚 Envío GRATIS a todo Colombia\n\n"
        mensaje += "Gracias por tu compra! 😊"
        
        # Asegurar que el string mantenga encoding UTF-8
        return mensaje