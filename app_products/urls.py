from django.urls import path
from .views import  ProductDetailView

urlpatterns = [
    path('<slug:slug>/p/<int:id>/', ProductDetailView.as_view(), name="product_detail"),

]
