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

    
class ProductDetailView(DetailView):
    model = Product
    template_name = "Product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Obtener todas las variantes activas con sus relaciones
        variants = (
            product.variants
            .filter(is_active=True)
            .prefetch_related(
                "options__option_value__option",
                "images"
            )
            .order_by("sku")
        )

        # Variante principal (primera activa)
        main_variant = variants.first()

        # Recopilar TODAS las imágenes de TODAS las variantes activas
        all_variant_images = []
        seen_urls = set()
        
        for variant in variants:
            for img in variant.images.all():
                # ✅ CAMBIO: usar .url del ImageField
                image_url = img.image_url.url if img.image_url else None
                
                if image_url and image_url not in seen_urls:
                    all_variant_images.append({
                        'url': image_url,
                        'alt': img.alt_text or f"{product.name} - {variant.sku}",
                        'variant_id': variant.id,
                        'is_main': img.is_main
                    })
                    seen_urls.add(image_url)

        # Ordenar: primero las imágenes principales
        all_variant_images.sort(key=lambda x: (not x['is_main'], x['url']))

        # ✅ DETECTAR QUÉ OPCIONES TIENE EL PRODUCTO
        available_options = {}
        for variant in variants:
            for variant_option in variant.options.all():
                option_name = variant_option.option_value.option.name
                if option_name not in available_options:
                    available_options[option_name] = True

        context.update({
            "variants": variants,
            "main_variant": main_variant,
            "all_variant_images": all_variant_images,
            "main_image": all_variant_images[0] if all_variant_images else None,
            
            # ✅ OPCIONES DISPONIBLES
            "has_color": "Color" in available_options,
            "has_medida": "Medida" in available_options,
            "has_peso": "Peso" in available_options,
            "has_material": "Material" in available_options,
            
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