from .dropi import dropi_login, dropi_get_products
from app_products.models import Product, ProductVariant

def sync_dropi_products():
    token = dropi_login()
    dropi_products = dropi_get_products(token)

    for p in dropi_products:

        # 1. Crear o actualizar producto
        product_obj, created = Product.objects.update_or_create(
            provider_product_id=p["id"],
            defaults={
                "name": p["name"],
                "description": p.get("description", ""),
                "price": p["price"],
                "image": p["image"] if p.get("image") else None
            }
        )

        # 2. Borrar variantes existentes para actualizar
        product_obj.variants.all().delete()

        # 3. Guardar variantes nuevas
        for v in p.get("variants", []):
            ProductVariant.objects.create(
                product=product_obj,
                name=v["name"],
                value=v["value"],
                extra_price=v.get("extra_price", 0),
                provider_variant_id=v["id"]  # ID de Dropi
            )

    return True
