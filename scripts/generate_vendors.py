import json
import random
import os

os.makedirs("data", exist_ok=True)

locations = ["Chennai", "Coimbatore", "Madurai", "Trichy"]

venue_names = [
    "Grand Palace Hall", "Royal Convention Center", "Green Garden Banquet",
    "Marina Wedding Hall", "Elite Event Arena", "Golden Lotus Hall",
    "Skyline Convention Hall", "Palm Grove Banquet", "Silver Crown Venue",
    "Harmony Event Center", "Crystal Hall", "Blue Orchid Venue",
    "Lake View Banquet", "Emerald Hall", "Sunrise Convention Center",
    "Prestige Palace", "Star Banquet", "Moonlight Hall",
    "Infinity Arena", "Celebration Center"
]

caterer_names = [
    "Elite Caterers", "Royal Feast Catering", "South Spice Catering",
    "Chennai Foods", "Grand Buffet Services", "Heritage Caterers",
    "Annapoorna Catering", "Tasty Treats", "Premium Plates",
    "Classic Catering Co", "Golden Spoon", "Food Fiesta",
    "Flavour Masters", "Traditional Taste", "Happy Meals",
    "Luxury Catering", "Spice Route", "Delight Caterers",
    "Fresh Feast", "Silver Plate Catering"
]

decorator_names = [
    "Dream Decorators", "Elegant Events", "Floral Creations",
    "Grand Decor Studio", "Magic Moments Decor", "Royal Decor",
    "Blossom Events", "Creative Decorators", "Event Designers",
    "Golden Themes", "Wedding Wonders", "Premium Decor",
    "Party Makers", "Elegant Themes", "Vision Decor"
]

photographer_names = [
    "Pixel Photography", "Lens Masters", "Focus Studio",
    "Capture Moments", "Vision Photography", "Dream Lens",
    "Wedding Clicks", "Perfect Frames", "Shutter Stories",
    "Golden Memories", "Elite Photography", "Moment Makers",
    "Studio One", "PhotoCraft", "Frame Factory"
]


def create_vendor(
    vendor_id,
    name,
    vendor_type,
    min_price,
    max_price,
    min_capacity,
    max_capacity
):
    return {
        "id": vendor_id,
        "name": name,
        "vendor_type": vendor_type,
        "location": random.choice(locations),
        "price": random.randint(min_price, max_price),
        "capacity": random.randint(min_capacity, max_capacity),
        "rating": round(random.uniform(3.8, 5.0), 1),
        "available": random.choice([True, True, True, False])
    }


vendors = []

# 20 Venues
for i, name in enumerate(venue_names, start=101):
    vendors.append(
        create_vendor(
            i,
            name,
            "venue",
            50000,
            150000,
            100,
            1000
        )
    )

# 20 Caterers
for i, name in enumerate(caterer_names, start=201):
    vendors.append(
        create_vendor(
            i,
            name,
            "catering",
            20000,
            80000,
            100,
            1000
        )
    )

# 15 Decorators
for i, name in enumerate(decorator_names, start=301):
    vendors.append(
        create_vendor(
            i,
            name,
            "decoration",
            10000,
            60000,
            500,
            1000
        )
    )

# 15 Photographers
for i, name in enumerate(photographer_names, start=401):
    vendors.append(
        create_vendor(
            i,
            name,
            "photography",
            15000,
            75000,
            500,
            1000
        )
    )

with open("data/vendors.json", "w") as file:
    json.dump(vendors, file, indent=4)

print(f"Generated {len(vendors)} vendors successfully!")