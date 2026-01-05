from django.urls import path
from app_products import views

urlpatterns = [
    path('', views.AllProductDetailView.as_view(), name="all_products"),
    path('<slug:slug>/p/<int:id>/', views.ProductDetailView.as_view(), name="product_detail"),


]
