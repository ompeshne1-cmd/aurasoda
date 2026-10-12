import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from .models import Category, Product, Review, Order, OrderItem, ContactMessage, NewsletterSubscriber
from .forms import ReviewForm, CheckoutForm, ContactForm, NewsletterForm
from .cart import Cart


def index(request):
    featured_products = Product.objects.filter(is_featured=True)[:4]
    all_products = Product.objects.all()[:6]
    categories = Category.objects.all()
    recent_reviews = Review.objects.select_related("product").all()[:4]

    context = {
        "featured_products": featured_products,
        "all_products": all_products,
        "categories": categories,
        "recent_reviews": recent_reviews,
    }
    return render(request, "store/index.html", context)


def shop(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    # Category Filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Search Query
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(tasting_notes__icontains=query)
            | Q(tagline__icontains=query)
        )

    # Sorting
    sort_by = request.GET.get("sort", "featured")
    if sort_by == "price_low":
        products = products.order_by("price")
    elif sort_by == "price_high":
        products = products.order_by("-price")
    elif sort_by == "name":
        products = products.order_by("name")
    elif sort_by == "bestseller":
        products = products.order_by("-is_bestseller", "-created_at")
    else:
        products = products.order_by("-is_featured", "-created_at")

    context = {
        "current_category": category,
        "categories": categories,
        "products": products,
        "query": query,
        "sort_by": sort_by,
        "product_count": products.count(),
    }
    return render(request, "store/shop.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]
    reviews = product.reviews.all()

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.save()
            messages.success(request, "Thank you! Your tasting review has been shared.")
            return redirect("store:product_detail", slug=product.slug)
    else:
        review_form = ReviewForm()

    context = {
        "product": product,
        "related_products": related_products,
        "reviews": reviews,
        "review_form": review_form,
    }
    return render(request, "store/product_detail.html", context)


def cart_detail(request):
    cart = Cart(request)
    subtotal = cart.get_subtotal()
    shipping = cart.get_shipping()
    total = cart.get_total()

    # Free shipping threshold ($40)
    free_shipping_needed = max(0.0, round(40.0 - subtotal, 2))
    shipping_progress = min(100, int((subtotal / 40.0) * 100)) if subtotal > 0 else 0

    context = {
        "cart": cart,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
        "free_shipping_needed": free_shipping_needed,
        "shipping_progress": shipping_progress,
    }
    return render(request, "store/cart.html", context)


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    pack = request.POST.get("pack", "single")
    quantity = int(request.POST.get("quantity", 1))

    cart.add(product=product, pack=pack, quantity=quantity)

    # Check for AJAX request
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "status": "success",
            "message": f"Added {quantity}x {product.name} to your crate.",
            "cart_count": len(cart),
            "cart_subtotal": cart.get_subtotal(),
        })

    messages.success(request, f"Added {quantity}x {product.name} to your crate.")
    return redirect(request.META.get("HTTP_REFERER", "store:cart_detail"))


def cart_update(request):
    if request.method == "POST":
        cart = Cart(request)
        item_key = request.POST.get("item_key")
        quantity = int(request.POST.get("quantity", 1))
        cart.update(item_key=item_key, quantity=quantity)
        messages.success(request, "Crate updated successfully.")
    return redirect("store:cart_detail")


def cart_remove(request, item_key):
    cart = Cart(request)
    cart.remove(item_key)
    messages.info(request, "Item removed from crate.")
    return redirect("store:cart_detail")


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your crate is empty. Please add some craft sodas first!")
        return redirect("store:shop")

    subtotal = cart.get_subtotal()
    shipping = cart.get_shipping()
    total = cart.get_total()

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_number = f"HB-{uuid.uuid4().hex[:6].upper()}"
            order.subtotal = subtotal
            order.shipping_fee = shipping
            order.total_amount = total
            order.save()

            # Create items
            for item in cart:
                product = get_object_or_404(Product, id=item["product_id"])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    pack_label=item["pack_label"],
                    unit_price=item["price"],
                    quantity=item["quantity"],
                    subtotal=item["item_total"],
                )

            # Clear cart
            cart.clear()
            request.session["last_order_id"] = order.id
            messages.success(request, f"Order #{order.order_number} confirmed! Thank you for supporting artisanal craft sodas.")
            return redirect("store:order_success", order_number=order.order_number)
    else:
        form = CheckoutForm()

    context = {
        "cart": cart,
        "form": form,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    }
    return render(request, "store/checkout.html", context)


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, "store/order_success.html", {"order": order})


def about(request):
    return render(request, "store/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your dispatch was received! Our brewmaster will respond shortly.")
            return redirect("store:contact")
    else:
        form = ContactForm()
    return render(request, "store/contact.html", {"form": form})


def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if email:
            obj, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Welcome to the Craft Guild! You'll receive private micro-batch release notes.")
            else:
                messages.info(request, "You are already a subscriber to our brew logs.")
    return redirect(request.META.get("HTTP_REFERER", "store:index"))
