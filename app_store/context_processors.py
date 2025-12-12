from app_products.models import Category

def categorias_globales(request):
    return {
        "categorias": Category.objects.all()
    }
