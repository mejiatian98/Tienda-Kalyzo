from django.urls import path
from app_store import views

urlpatterns = [
    path("", views.StoreView.as_view(), name="store_page"),
    path("categorias/", views.CategoriaView.as_view(), name="categorys"),
    path("categorias/<slug:slug>/", views.CategoriaProductosView.as_view(),name="category_products"),
    path("nuevos productos/", views.NewsProductsView.as_view(), name="news_products"),
    path("buscar/", views.SearchProductsView.as_view(), name="search_products"),
    path("top ventas/", views.TopSellingProductsView.as_view(), name="top_selling_products"),
    path("productos oferta/", views.DiscountedProductsView.as_view(), name="discounted_products"),

    
    
    
]
