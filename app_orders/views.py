from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from app_products.models import ProductVariant, Product
from .utils.cart import Cart

# Carrito Views
class CarritoView(TemplateView):
    """
    Vista principal del carrito
    """
    template_name = 'carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        producto = Product.objects.all()
        # Traer el slug y id del producto
        
        context.update({
            'cart_items': cart.get_items(),
            'cart_total': cart.get_total(),
            'cart_count': cart.get_count(),
            'cart_savings': cart.get_savings(),  # ✅ AGREGAR
            'cart_subtotal': cart.get_subtotal(),
        })
        
        
        return context 

# Agregar producto al carrito (AJAX)
class AddToCartView(View):
    """
    Vista para agregar productos al carrito (AJAX)
    """
    
    def post(self, request, *args, **kwargs):
        variant_id = request.POST.get('variant_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if not variant_id:
            return JsonResponse({
                'success': False,
                'message': 'Producto no especificado'
            }, status=400)
        
        cart = Cart(request)
        success, message = cart.add(variant_id, quantity)
        
        response = JsonResponse({
            'success': success,
            'message': message,
            'cart_count': cart.get_count(),
            'cart_total': float(cart.get_total())
        })
        
        if success:
            cart.save_to_response(response)
        
        return response

# Actualizar cantidades en el carrito (AJAX)
class UpdateCartView(View):
    """
    Vista para actualizar cantidades en el carrito
    """
    
    def post(self, request, *args, **kwargs):
        variant_id = request.POST.get('variant_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart = Cart(request)
        success, message = cart.update(variant_id, quantity)
        
        response = JsonResponse({
            'success': success,
            'message': message,
            'cart_count': cart.get_count(),
            'cart_total': float(cart.get_total())
        })
        
        if success:
            cart.save_to_response(response)
        
        return response

# Eliminar productos del carrito (AJAX)
class RemoveFromCartView(View):
    """
    Vista para eliminar productos del carrito
    """
    
    def post(self, request, *args, **kwargs):
        variant_id = request.POST.get('variant_id')
        
        cart = Cart(request)
        success, message = cart.remove(variant_id)
        
        response = JsonResponse({
            'success': success,
            'message': message,
            'cart_count': cart.get_count(),
            'cart_total': float(cart.get_total())
        })
        
        if success:
            cart.save_to_response(response)
        
        return response

# Vaciar el carrito (AJAX)
class ClearCartView(View):
    """
    Vista para vaciar el carrito completamente
    """
    
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        success, message = cart.clear()
        
        response = JsonResponse({
            'success': success,
            'message': message,
            'cart_count': 0,
            'cart_total': 0
        })
        
        if success:
            cart.save_to_response(response)
        
        return response

# Obtener el contador del carrito (AJAX)
class GetCartCountView(View):
    """
    Vista para obtener el contador del carrito (para actualizar el header)
    """
    
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        
        return JsonResponse({
            'cart_count': cart.get_count(),
            'cart_total': float(cart.get_total())
        })
    
# Obtener los items del carrito (AJAX)
class GetCartItemsView(View):
    """
    Vista para obtener los items del carrito en formato JSON
    """
    def get(self, request):
        cart = Cart(request)
        
        return JsonResponse({
            'items': cart.get_items(),
            'cart_count': cart.get_count(),
            'subtotal': cart.get_subtotal(),
            'total': cart.get_total(),
            'savings': cart.get_savings(),
        })