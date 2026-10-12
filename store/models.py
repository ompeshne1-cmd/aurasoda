from django.db import models
from django.urls import reverse
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    badge = models.CharField(max_length=50, blank=True, help_text="e.g. 'Barrel Aged', 'Herbal Tonic'")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:shop_category", kwargs={"category_slug": self.slug})


class Product(models.Model):
    PACK_CHOICES = (
        ("single", "Single Bottle (355ml)"),
        ("four", "4-Pack Craft Box"),
        ("case", "Collector's Case (12-Pack)"),
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    tagline = models.CharField(max_length=200, help_text="Short poetic descriptor")
    description = models.TextField()
    tasting_notes = models.CharField(max_length=255, help_text="Comma-separated tasting notes")
    ingredients = models.TextField(help_text="Key botanicals and ingredients")
    pairing_notes = models.CharField(max_length=255, blank=True, help_text="e.g. Charred meats, artisan cheeses")

    # Pricing per pack
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Single bottle price")
    price_four_pack = models.DecimalField(max_digits=6, decimal_places=2, default=16.99, help_text="4-pack price")
    price_case = models.DecimalField(max_digits=6, decimal_places=2, default=45.99, help_text="12-pack case price")

    # Assets & details
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    static_image_name = models.CharField(max_length=100, default="the_cinder.jpg", help_text="Static image filename fallback")
    volume_ml = models.PositiveIntegerField(default=355)
    carbonation_level = models.CharField(max_length=50, default="Medium Crisp Effervescence")
    sugar_content = models.CharField(max_length=50, default="18g Organic Cane Sugar")

    # Status
    stock = models.PositiveIntegerField(default=100)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={"slug": self.slug})

    @property
    def tasting_notes_list(self):
        return [note.strip() for note in self.tasting_notes.split(",") if note.strip()]

    def average_rating(self):
        avg = self.reviews.aggregate(Avg("rating"))["rating__avg"]
        return round(avg, 1) if avg else 5.0

    def review_count(self):
        return self.reviews.count()

    def get_image_url(self):
        if self.image:
            return self.image.url
        return f"/static/store/images/{self.static_image_name}"

    def get_price(self, pack="single"):
        if pack == "four":
            return self.price_four_pack
        elif pack == "case":
            return self.price_case
        return self.price


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, f"{i} Stars") for i in range(1, 6)])
    title = models.CharField(max_length=150)
    comment = models.TextField()
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author_name} on {self.product.name} ({self.rating}★)"


class Order(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    )
    PAYMENT_CHOICES = (
        ("cod", "Cash on Delivery"),
        ("card", "Credit / Debit Card (Simulated)"),
        ("upi", "UPI / QR Payment (Simulated)"),
    )

    order_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    notes = models.TextField(blank=True)

    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default="cod")
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.order_number} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pack_label = models.CharField(max_length=50, default="Single Bottle")
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} ({self.pack_label})"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}: {self.subject}"
