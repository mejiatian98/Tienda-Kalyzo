from django.shortcuts import render
from django.views import View
from app_products.models import Product, Category
from django.shortcuts import get_object_or_404

# Pagina de la tienda
class StoreView(View):
    def get(self, request):
        productos = Product.objects.order_by('?')   # 🔥 orden aleatorio
        return render(request, "store_page.html", {"productos": productos})


# Vista para mostrar las categorías con sus productos
class CategoriaView(View):
    def get(self, request):

        categorias = Category.objects.prefetch_related("products__images").all()

        context = {
            "categorias": categorias
        }

        return render(request, "Categoria_products.html", context)


# Vista para mostrar productos de una categoría específica
class CategoriaProductosView(View):
    def get(self, request, slug, id):

        # Buscar la categoría por ID
        categoria = get_object_or_404(Category, id=id)

        # Filtrar los productos de esa categoría
        productos = (
            Product.objects
            .filter(category=categoria)
            .prefetch_related("images")
        )

        # 🔥 Listado de todas las categorías (para el sidebar)
        categorias = Category.objects.all()

        context = {
            "categoria": categoria,
            "productos": productos,
            "categorias": categorias,   # 👈 Añadido sin romper nada
        }

        return render(request, "Pages_category.html", context)


# Vista para mostrar los productos más nuevos
class NewsProductsView(View):
    def get(self, request):
        # Traer los productos ordenados por fecha de creación (más nuevos primero)
        productos_nuevos = Product.objects.order_by('-created_at')

        return render(request, "news_products.html", {
            "productos": productos_nuevos
        })
    

# Busqueda de productos
class SearchProductsView(View):
    def get(self, request):
        query = request.GET.get("q", "")

        productos = Product.objects.filter(
            name__icontains=query
        ).prefetch_related("images")

        return render(request, "search_results.html", {
            "query": query,
            "productos": productos
        })


# Vista para mostrar los productos más vendidos
class TopSellingProductsView(View):
    def get(self, request):
        # Traer los productos ordenados por ventas (más vendidos primero)
        productos_top_ventas = Product.objects.order_by('-sales_count')

        return render(request, "top_selling_products.html", {
            "productos": productos_top_ventas
        })
    

# Vista para mostrar solo productos con descuento
class DiscountedProductsView(View):
    def get(self, request):

        # Traer solo productos donde discount_price no sea None y sea mayor que 0
        productos= Product.objects.filter(
            discount_price__isnull=False,
            discount_price__gt=0
        ).prefetch_related("images")

        context = {
            "productos": productos
        }

        return render(request, "Discounted_products.html", context)
