from django.urls import path
from app_store import views

urlpatterns = [
    path("", views.StoreView.as_view(), name="store_page"),
    path("productos/categorias/", views.CategoriaView.as_view(), name="categorys"),
    path("productos/categorias/<slug:slug>/", views.CategoriaProductosView.as_view(),name="category_products"),
    path("productos/nuevos productos/", views.NewsProductsView.as_view(), name="news_products"),
    path("productos/buscar/", views.SearchProductsView.as_view(), name="search_products"),
    path("productos/top ventas/", views.TopSellingProductsView.as_view(), name="top_selling_products"),
    path("productos/productos oferta/", views.DiscountedProductsView.as_view(), name="discounted_products"),

    
]
