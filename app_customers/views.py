# app_customers/views.py
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
import json

from .forms import CustomerOrderForm
from .services import OrderService

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CreateOrderView(View):
    """Vista para crear una orden con soporte completo UTF-8 para emojis"""
    
    def post(self, request, *args, **kwargs):
        """Procesar creación de orden"""
        try:
            # 1. Parsear datos JSON con encoding UTF-8 explícito
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
            
            # 2. Validar formulario
            form = CustomerOrderForm(data)
            
            if not form.is_valid():
                return JsonResponse({
                    'success': False,
                    'message': 'Datos inválidos',
                    'errors': form.errors
                }, status=400, json_dumps_params={'ensure_ascii': False})
            
            # 3. Crear orden usando el servicio
            order, whatsapp_message, success, error = OrderService.create_order_from_cart(
                request,
                form.cleaned_data
            )
            
            if not success:
                return JsonResponse({
                    'success': False,
                    'message': error
                }, status=400, json_dumps_params={'ensure_ascii': False})
            
            # 4. Retornar respuesta exitosa con UTF-8
            return JsonResponse({
                'success': True,
                'message': 'Orden creada exitosamente',
                'data': {
                    'order_id': order.id,
                    'whatsapp_message': whatsapp_message,
                    'whatsapp_number': '573217618510',
                    'total': str(order.total)
                }
            }, json_dumps_params={'ensure_ascii': False}, content_type='application/json; charset=utf-8')
        
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Datos JSON inválidos'
            }, status=400, json_dumps_params={'ensure_ascii': False})
        
        except Exception as e:
            import traceback
            print(f"Error en CreateOrderView: {e}")
            print(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': f'Error inesperado: {str(e)}'
            }, status=500, json_dumps_params={'ensure_ascii': False})