from django.views.generic import DetailView
from .models import Product


# Detalle del producto
class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.object

        # Variantes
        context["variants"] = product.variants.all()

        # Imágenes
        context["images"] = product.images.all()

        # Productos similares (listos para el Card.html)
        context["productos"] = (
            Product.objects.filter(category=product.category)
            .exclude(id=product.id)
        )[:4]

        return context
