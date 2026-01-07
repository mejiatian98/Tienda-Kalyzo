from django.views.generic import DetailView
from .models import Product, CommentPublic
from django.shortcuts import redirect, render
from django.views import View




# Mostrar todos los productos
class AllProductDetailView(View):
    def get(self, request):
        productos = Product.objects.filter(is_active=True).order_by("?")
        return render(
            request,
            "All_Products.html",
            {"productos": productos}
        )

    

    
# Detalle del producto
class ProductDetailView(DetailView):
    model = Product
    template_name = "Product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        variants = (
            product.variants
            .filter(is_active=True)
            .prefetch_related(
                "options__option_value__option",
                "images"
            )
        )

        main_variant = variants.first()

        context.update({
            "variants": variants,
            "main_variant": main_variant,
            "images": main_variant.images.all() if main_variant else [],
            "has_medida": variants.filter(
                options__option_value__option__name="Medida"
            ).exists(),
            "productos": (
                Product.objects
                .filter(category=product.category, is_active=True)
                .exclude(id=product.id)[:4]
            ),
            "comments": product.comments.all().order_by("-created_at"),
        })

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

        return redirect(
            "product_detail",
            slug=product.slug,
            id=product.id
        )


