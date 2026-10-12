from .models import Category


def cart_and_categories(request):
    """
    Context processor to make categories and session cart summary
    available across all templates.
    """
    categories = Category.objects.all()
    cart = request.session.get("cart", {})

    total_items = 0
    subtotal = 0.0

    for item_key, item in cart.items():
        qty = item.get("quantity", 0)
        price = float(item.get("price", 0.0))
        total_items += qty
        subtotal += qty * price

    return {
        "all_categories": categories,
        "cart_count": total_items,
        "cart_subtotal": round(subtotal, 2),
    }
