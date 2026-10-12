from django.core.management.base import BaseCommand
from store.models import Category, Product, Review


class Command(BaseCommand):
    help = "Seeds initial heritage craft soda products, categories, and sommelier reviews"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding heritage craft soda catalog..."))

        # 1. Categories
        cat_barrel, _ = Category.objects.get_or_create(
            slug="barrel-aged-reserves",
            defaults={
                "name": "Barrel Aged Reserves",
                "description": "Slow-matured sodas infused with toasted oak, rich dark spices, and bourbon vanilla.",
                "badge": "Oak Matured",
            },
        )

        cat_citrus, _ = Category.objects.get_or_create(
            slug="citrus-fruit-elixirs",
            defaults={
                "name": "Citrus & Fruit Elixirs",
                "description": "Cold-pressed orchard fruit, sun-drenched citrus zest, and aromatic garden herbs.",
                "badge": "Fresh Pressed",
            },
        )

        cat_ginger, _ = Category.objects.get_or_create(
            slug="spice-herbal-brews",
            defaults={
                "name": "Spice & Herbal Brews",
                "description": "Fiery organic root ginger, steeped botanicals, and raw golden wildflower honey.",
                "badge": "Kettle Brewed",
            },
        )

        cat_botanical, _ = Category.objects.get_or_create(
            slug="botanical-tonics",
            defaults={
                "name": "Botanical Tonics",
                "description": "Delicate floral essences, culinary herbs, and crisp artisan sparkling spring water.",
                "badge": "Wild Harvest",
            },
        )

        # 2. Products
        products_data = [
            {
                "name": "The Cinder Spiced Vanilla & Oak",
                "slug": "the-cinder-spiced-vanilla-oak",
                "category": cat_barrel,
                "tagline": "Caramelized Cane Sugar, Charred French Oak & Madagascar Vanilla",
                "description": "A dark, mesmerizing craft soda steeped with toasted American oak spirals and whole Madagascar bourbon vanilla pods. Deeply aromatic with notes of dark toffee, gentle smoke, and velvety wood tannins that dance on the palate.",
                "tasting_notes": "French Oak, Dark Toffee, Madagascar Vanilla, Star Anise",
                "ingredients": "Carbonated Artisan Spring Water, Pure Cane Sugar, Madagascar Vanilla Bean Extract, Natural Oak Wood Extract, Star Anise Infusion, Citric Acid.",
                "pairing_notes": "Smoked brisket, aged Gouda, dark chocolate truffles",
                "price": 4.50,
                "price_four_pack": 16.99,
                "price_case": 46.99,
                "static_image_name": "the_cinder.jpg",
                "volume_ml": 355,
                "carbonation_level": "Velvety Champagne Bubbles",
                "sugar_content": "19g Organic Cane Sugar",
                "stock": 140,
                "is_featured": True,
                "is_bestseller": True,
                "reviews": [
                    {
                        "author_name": "Julian Vance",
                        "rating": 5,
                        "title": "Unrivaled depth of flavor",
                        "comment": "Unlike any grocery soda on earth. The charred oak nuance cuts right through the vanilla sweetness with mature elegance. An instant bar staple.",
                    },
                    {
                        "author_name": "Elena Rostova",
                        "rating": 5,
                        "title": "Rich and smoky perfection",
                        "comment": "Served chilled over a single large sphere of clear ice. The aroma fills the room before the first sip. Absolutely exquisite.",
                    },
                ],
            },
            {
                "name": "Ruby Gloom Blood Orange & Rosemary",
                "slug": "ruby-gloom-blood-orange-rosemary",
                "category": cat_citrus,
                "tagline": "Sicilian Moro Blood Orange with Crushed Wild Rosemary & Ginger",
                "description": "Vibrant, tart, and deeply refreshing. Sourced from organic Sicilian blood oranges and blended with freshly harvested crushed rosemary sprigs. The effervescence releases citrus oils that elevate both casual afternoons and celebratory dining.",
                "tasting_notes": "Crimson Blood Orange, Wild Rosemary, Cold-Pressed Ginger, Tart Pomegranate",
                "ingredients": "Carbonated Spring Water, Sicilian Blood Orange Puree (12%), Fair Trade Cane Sugar, Fresh Rosemary Distillate, Ginger Root Extract, Organic Lemon Juice.",
                "pairing_notes": "Roasted duck breast, goat cheese crostini, Mediterranean mezze",
                "price": 4.75,
                "price_four_pack": 17.50,
                "price_case": 48.50,
                "static_image_name": "ruby_gloom.jpg",
                "volume_ml": 355,
                "carbonation_level": "Crisp Bright Carbonation",
                "sugar_content": "16g Cold-Pressed Fruit Sugar",
                "stock": 95,
                "is_featured": True,
                "is_bestseller": True,
                "reviews": [
                    {
                        "author_name": "Marcus Thorne",
                        "rating": 5,
                        "title": "A masterclass in botanical soda",
                        "comment": "The rosemary gives it an earthy, sophisticated backbone that balances the zesty blood orange. Truly a five-star craft experience.",
                    },
                    {
                        "author_name": "Sarah Lin",
                        "rating": 5,
                        "title": "My daily afternoon ritual",
                        "comment": "Gorgeous color in the glass, incredible aroma. Not cloyingly sweet, perfectly balanced acidity.",
                    },
                ],
            },
            {
                "name": "Golden Ginger Lemongrass & Wild Honey",
                "slug": "golden-ginger-lemongrass-wild-honey",
                "category": cat_ginger,
                "tagline": "Fiery Hawaiian Ginger, Fragrant Lemongrass & Mountain Wildflower Honey",
                "description": "A copper-kettle ginger soda brewed with cold-pressed ginger root that delivers an authentic, warming spice. Layered with aromatic Thai lemongrass stalks and smoothed by rich raw honey harvested from high alpine meadows.",
                "tasting_notes": "Warming Ginger Spice, Crisp Lemongrass, Wildflower Honey, Key Lime",
                "ingredients": "Spring Water, Fresh Pressed Hawaiian Ginger Juice, Alpine Wildflower Honey, Organic Cane Sugar, Steamed Lemongrass Infusion, Key Lime Juice, Sea Salt.",
                "pairing_notes": "Thai curries, artisan sushi, glazed pork belly, spiced nuts",
                "price": 4.50,
                "price_four_pack": 16.99,
                "price_case": 46.99,
                "static_image_name": "golden_ginger.jpg",
                "volume_ml": 355,
                "carbonation_level": "Punchy Micro-Effervescence",
                "sugar_content": "17g Honey & Cane Blend",
                "stock": 110,
                "is_featured": True,
                "is_bestseller": False,
                "reviews": [
                    {
                        "author_name": "Chef David Sterling",
                        "rating": 5,
                        "title": "Real ginger with authentic fire",
                        "comment": "You can taste the actual ginger root particles and pure lemongrass oils. A proper craft ginger brew that leaves supermarket brands far behind.",
                    },
                ],
            },
            {
                "name": "Velvet Barrel Aged Bourbon Cream",
                "slug": "velvet-barrel-aged-bourbon-cream",
                "category": cat_barrel,
                "tagline": "Charred Cask Smoked Cream Soda with Pure Tahitian & Bourbon Vanilla",
                "description": "An opulent homage to 19th-century cream sodas. Brewed with creamy sweet butterscotch notes, roasted marshmallow undertones, and resting atop mellow Kentucky oak barrel extracts. Smooth as liquid velvet.",
                "tasting_notes": "Whipped Sweet Cream, Charred Oak Stave, Caramelized Sugar, Bourbon Vanilla",
                "ingredients": "Carbonated Artesian Well Water, Pure Evaporated Cane Juice, Toasted Vanilla Bean Caviar, Natural Oak Flavors, Caramelized Sugar, Citric Acid.",
                "pairing_notes": "Pecan pie, grilled peach cobbler, sharp farmhouse cheddar",
                "price": 4.95,
                "price_four_pack": 18.50,
                "price_case": 51.00,
                "static_image_name": "velvet_barrel.jpg",
                "volume_ml": 500,
                "carbonation_level": "Silk Micro-Foam",
                "sugar_content": "21g Pure Cane Sugar",
                "stock": 80,
                "is_featured": True,
                "is_bestseller": True,
                "reviews": [
                    {
                        "author_name": "Clara Beauchamp",
                        "rating": 5,
                        "title": "Pure liquid nostalgia with modern refinement",
                        "comment": "I cannot drink normal cream sodas anymore after this. The smoky barrel essence makes this an experience worth savoring slowly.",
                    },
                ],
            },
            {
                "name": "Violet Mist Wild Lavender & Meyer Lemon",
                "slug": "violet-mist-wild-lavender-meyer-lemon",
                "category": cat_botanical,
                "tagline": "Delicate English Lavender Blossoms with Sun-Ripened Meyer Lemon",
                "description": "Crafted from steam-distilled organic culinary lavender flowers and bright California Meyer lemons. Soft, floral, effervescent, and luminous. An ethereal sparkling beverage that refreshes the soul.",
                "tasting_notes": "French Lavender, Meyer Lemon Peel, White Peach, Crushed Thyme",
                "ingredients": "Sparkling Mountain Spring Water, Organic Meyer Lemon Juice, Hand-Harvested Lavender Floral Extract, Golden Cane Sugar, White Grape Essence.",
                "pairing_notes": "Lemon herb roasted chicken, goat cheese salads, almond pastries",
                "price": 4.75,
                "price_four_pack": 17.50,
                "price_case": 48.50,
                "static_image_name": "violet_mist.jpg",
                "volume_ml": 330,
                "carbonation_level": "Delicate Champagne Fizz",
                "sugar_content": "14g Light Cane Sugar",
                "stock": 65,
                "is_featured": False,
                "is_bestseller": False,
                "reviews": [
                    {
                        "author_name": "Camille Monet",
                        "rating": 5,
                        "title": "A garden dream in a bottle",
                        "comment": "The lavender is subtle and culinary, never soapy. Beautiful pale shimmer when poured into a coupe glass.",
                    },
                ],
            },
        ]

        for p_data in products_data:
            reviews_data = p_data.pop("reviews", [])
            product, created = Product.objects.update_or_create(
                slug=p_data["slug"],
                defaults=p_data,
            )
            for r_data in reviews_data:
                Review.objects.get_or_create(
                    product=product,
                    author_name=r_data["author_name"],
                    defaults={
                        "rating": r_data["rating"],
                        "title": r_data["title"],
                        "comment": r_data["comment"],
                        "is_verified": True,
                    },
                )
            status_txt = "Created" if created else "Updated"
            self.stdout.write(f" - [{status_txt}] {product.name}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded Heritage Brew products, categories, and reviews!"))
