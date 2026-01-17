# app_customers/urls.py

from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    # ... tus rutas existentes ...
    
    # ✅ NUEVA RUTA - Crear orden desde checkout
    path('orden/crear/', views.CreateOrderView.as_view(), name='create_order'),
]