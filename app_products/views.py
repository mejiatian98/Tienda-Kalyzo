from django.views.generic import DetailView
from .models import Product, CommentPublic
from django.shortcuts import redirect
from django.views import View


class ProductDetailView(DetailView):
    model = Product
    template_name = "Product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Variantes activas
        variants = product.variants.filter(is_active=True)
        context["variants"] = variants

        # Variante principal (primera)
        main_variant = variants.first()
        context["main_variant"] = main_variant

        # Imágenes de la variante principal
        context["images"] = (
            main_variant.images.all() if main_variant else []
        )

        # Productos similares
        context["productos"] = (
            Product.objects
            .filter(category=product.category, is_active=True)
            .exclude(id=product.id)
        )[:4]

        # Comentarios
        comments = product.comments.all().order_by("-created_at")
        context["comments"] = comments

        context["avg_rating"] = (
            round(sum(c.rating for c in comments) / comments.count(), 1)
            if comments.exists()
            else 0
        )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = self.object

        name = request.POST.get("name")
        comment_text = request.POST.get("comment")
        rating = request.POST.get("rating")

        if name and comment_text and rating:
            CommentPublic.objects.create(
                product=product,
                name=name,
                comment=comment_text,
                rating=int(rating)
            )

        return redirect("Product_detail", slug=product.slug, id=product.id)