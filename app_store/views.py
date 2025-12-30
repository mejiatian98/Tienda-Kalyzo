from django.shortcuts import render
from django.views import View
from django.db.models import Prefetch
from app_products.models import Product, Category, ProductVariant
from django.shortcuts import get_object_or_404

# Pagina principal de la tienda
class StoreView(View):
    def get(self, request):
        productos = (
            Product.objects
            .filter(is_active=True)
            .prefetch_related(
                Prefetch(
                    "variants",
                    queryset=ProductVariant.objects.filter(is_active=True).prefetch_related("images")
                )
            )
            .order_by("?")
        )

        return render(request, "store_page.html", {"productos": productos})


# Vista para mostrar las categorías con sus productos
class CategoriaView(View):
    def get(self, request):
        categorias = Category.objects.prefetch_related(
            "products__variants__images",
            "products__variants"
        ).filter(products__is_active=True).distinct()

        context = {
            "categorias": categorias
        }

        return render(request, "Categoria_products.html", context)


# Vista para mostrar productos de una categoría específica
class CategoriaProductosView(View):
    def get(self, request, slug, id):
        # Buscar la categoría por ID
        categoria = get_object_or_404(Category, id=id)

        # Filtrar los productos de esa categoría con sus variantes e imágenes
        productos = (
            Product.objects
            .filter(is_active=True, category=categoria)
            .prefetch_related("variants__images", "variants")
        )

        # 🔥 Listado de todas las categorías (para el sidebar)
        categorias = Category.objects.filter(products__is_active=True).distinct()

        context = {
            "categoria": categoria,
            "productos": productos,
            "categorias": categorias,
        }

        return render(request, "Pages_category.html", context)


# Vista para mostrar los productos más nuevos
class NewsProductsView(View):
    def get(self, request):
        # Traer los productos ordenados por fecha de creación (más nuevos primero)
        productos_nuevos = Product.objects.order_by('-created_at').filter(is_active=True)

        return render(request, "news_products.html", {
            "productos": productos_nuevos
        })
    

# Busqueda de productos
class SearchProductsView(View):
    def get(self, request):
        query = request.GET.get("q", "")

        productos = Product.objects.filter(
            name__icontains=query,
            is_active=True
        ).prefetch_related("variants__images", "variants")

        return render(request, "search_results.html", {
            "query": query,
            "productos": productos
        })

# Vista para mostrar los productos más vendidos
class TopSellingProductsView(View):
    def get(self, request):
        # Traer los productos ordenados por ventas (más vendidos primero)
        productos_top_ventas = Product.objects.order_by('-sales_count').filter(is_active=True)

        return render(request, "top_selling_products.html", {
            "productos": productos_top_ventas
        })
    

# Vista para mostrar solo productos con descuento
class DiscountedProductsView(View):
    def get(self, request):
        # Traer productos que tengan al menos una variante con descuento activa
        productos = Product.objects.filter(
            is_active=True,
            variants__discount_price__isnull=False,
            variants__discount_price__gt=0,
            variants__is_active=True
        ).distinct().prefetch_related(
            'variants__images',
            'variants'
        )

        context = {
            "productos": productos
        }

        return render(request, "Discounted_products.html", context)