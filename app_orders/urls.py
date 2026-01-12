from django.urls import path
from app_orders import views
app_name = 'orders'

urlpatterns = [
    path('carrito/', views.CarritoView.as_view(), name='carrito'),
    path('carrito/agregar/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('carrito/actualizar/', views.UpdateCartView.as_view(), name='update_cart'),
    path('carrito/eliminar/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('carrito/vaciar/', views.ClearCartView.as_view(), name='clear_cart'),
    path('carrito/count/', views.GetCartCountView.as_view(), name='cart_count'),
]