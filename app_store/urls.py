from django.urls import path
from app_store import views

urlpatterns = [
    path("", views.StoreView.as_view(), name="store_page"),
    path("categorias/", views.CategoriaView.as_view(), name="category_products"),
    path("categoria_productos/<slug:slug>/c/<int:id>/kal-y-zo", views.CategoriaProductosView.as_view(), name="category_specific_products"),
    path("nuevos_productos/", views.NewsProductsView.as_view(), name="news_products"),
    path("buscar/", views.SearchProductsView.as_view(), name="search_products"),
    path("top_ventas/", views.TopSellingProductsView.as_view(), name="top_selling_products"),
    path("productos_oferta/", views.DiscountedProductsView.as_view(), name="discounted_products"),

    
    
    
]
