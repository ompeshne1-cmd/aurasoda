from decimal import Decimal
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, pack="single", quantity=1):
        product_id = str(product.id)
        item_key = f"{product_id}_{pack}"

        price_map = {
            "single": (float(product.price), "Single Bottle (355ml)"),
            "four": (float(product.price_four_pack), "4-Pack Box"),
            "case": (float(product.price_case), "12-Pack Collector's Case"),
        }

        unit_price, pack_label = price_map.get(pack, (float(product.price), "Single Bottle (355ml)"))

        if item_key not in self.cart:
            self.cart[item_key] = {
                "product_id": product.id,
                "name": product.name,
                "slug": product.slug,
                "pack": pack,
                "pack_label": pack_label,
                "price": unit_price,
                "quantity": 0,
                "image_url": product.get_image_url(),
            }

        self.cart[item_key]["quantity"] += int(quantity)
        self.save()

    def update(self, item_key, quantity):
        if item_key in self.cart:
            qty = int(quantity)
            if qty > 0:
                self.cart[item_key]["quantity"] = qty
            else:
                del self.cart[item_key]
            self.save()

    def remove(self, item_key):
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for key, item in self.cart.items():
            item_copy = item.copy()
            item_copy["key"] = key
            item_copy["item_total"] = round(item_copy["price"] * item_copy["quantity"], 2)
            yield item_copy

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_subtotal(self):
        return round(sum(item["price"] * item["quantity"] for item in self.cart.values()), 2)

    def get_shipping(self):
        subtotal = self.get_subtotal()
        if subtotal == 0:
            return 0.0
        # Free shipping over $40
        return 0.0 if subtotal >= 40.0 else 5.99

    def get_total(self):
        return round(self.get_subtotal() + self.get_shipping(), 2)
