from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def breadcrumbs(context):
    request = context['request']
    crumbs = []

    # Inicio
    crumbs.append({
        'name': 'Inicio',
        'url': '/'
    })

    resolver = request.resolver_match

    # =========================
    # CATEGORÍA ESPECÍFICA
    # =========================
    if resolver and resolver.url_name == 'category_specific_products':
        slug = resolver.kwargs.get('slug')

        crumbs.append({
            'name': slug.replace('-', ' ').capitalize(),
            'url': request.path
        })

        return crumbs

    # =========================
    # DETALLE DE PRODUCTO
    # =========================
    product = context.get('product') or context.get('object')

    if product and hasattr(product, 'category'):
        category = product.category

        crumbs.append({
            'name': category.name,
            'url': f'categorias/{category.slug}/'
        })

        crumbs.append({
            'name': product.name,
            'url': request.path
        })

        return crumbs

    # =========================
    # FALLBACK LIMPIO (SIN INTS)
    # =========================
    path_parts = [
        p for p in request.path.strip('/').split('/')
        if not p.isdigit() and p not in ['c', 'kal-y-zo']
    ]

    url = '/'
    for part in path_parts:
        url += part + '/'
        crumbs.append({
            'name': part.replace('-', ' ').capitalize(),
            'url': url
        })

    return crumbs
