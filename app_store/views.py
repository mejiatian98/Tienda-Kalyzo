from django.shortcuts import render
from django.views import View
from django.db.models import Prefetch
from app_products.models import Product, Category, ProductVariant
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models import Avg

# Pagina principal de la tienda
class StoreView(View):
    def get(self, request):

        variants_prefetch = Prefetch(
            "variants",
            queryset=ProductVariant.objects
                .filter(is_active=True)
                .prefetch_related("images")
        )

        featured_products = (
            Product.objects
            .filter(is_active=True, is_featured=True)
            .prefetch_related(variants_prefetch)
        )

        productos = (
            Product.objects
            .filter(is_active=True)
            .prefetch_related(variants_prefetch)
            .order_by("?")
        )

        return render(
            request,
            "store_page.html",
            {
                "featured_products": featured_products,
                "productos": productos,
            }
        )


# Vista para mostrar las categorías con sus productos
class CategoriaView(View):
    def get(self, request):
        categorias = (
            Category.objects
            .filter(products__is_active=True)
            .annotate(total_products=Count('products', distinct=True))
            .prefetch_related('products')
            .distinct()
        )

        context = {
            "categorias": categorias
        }

        return render(request, "Pages_category.html", context)


# Vista para mostrar productos de una categoría específica
class CategoriaProductosView(View):
    def get(self, request, slug):
        # Categoría seleccionada
        categoria = get_object_or_404(Category, slug=slug)

        # Productos activos de esa categoría
        productos = (
            Product.objects
            .filter(
                is_active=True,
                category=categoria,
                variants__is_active=True
            )
            .distinct()
            .prefetch_related(
                Prefetch(
                    "variants",
                    queryset=ProductVariant.objects.filter(is_active=True).prefetch_related("images")
                )
            )
        )

        context = {
            "categoria": categoria,
            "productos": productos,
        }

        return render(request, "Categoria_products.html", context)


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
    

# Vista para la página "Sobre Nosotros"
class sobreNosotros(View):
    def get(self, request):
        return render(request, "Sobre_nosotros.html")
    
    
# Vista para la página de Contacto
class ContactView(View):
    def get(self, request):
        return render(request, "Sobre_nosotros.html")
    
