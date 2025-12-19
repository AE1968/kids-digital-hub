import os
import json
import random
from datetime import datetime

# Configurare - citește din variabile de mediu
PRODUCT_COUNT = int(os.getenv('PRODUCT_COUNT', '5'))

# Teme pentru generare produse
THEMES = [
    "Space Adventure", "Underwater World", "Dinosaur Safari", "Fairy Tale Castle",
    "Robot Factory", "Jungle Explorer", "Arctic Animals", "Farm Friends",
    "Superhero Academy", "Magical Forest", "Pirate Treasure", "Dragon Kingdom",
    "Rainbow Unicorns", "Ocean Creatures", "Wild West", "Circus Fun",
    "Monster Friends", "Princess Palace", "Knight's Quest", "Wizard School"
]

CATEGORIES = ["Coloring", "Stories", "Games", "Worksheets"]

def generate_product_name(theme):
    """Generează un nume de produs bazat pe temă"""
    prefixes = ["Amazing", "Magical", "Super", "Fun", "Creative", "Exciting"]
    suffixes = ["Adventure", "Collection", "Pack", "Set", "Bundle", "Experience"]
    
    return f"{random.choice(prefixes)} {theme} {random.choice(suffixes)}"

def generate_products(count):
    """Generează produse noi"""
    products = []
    
    # Încarcă produsele existente pentru a continua ID-urile
    try:
        with open("js/products_data.js", "r", encoding="utf-8") as f:
            content = f.read()
            # Extrage JSON din fișierul JS
            json_str = content.replace("var allProducts = ", "").rstrip(";")
            existing_products = json.loads(json_str)
            next_id = max([p['id'] for p in existing_products]) + 1
    except (FileNotFoundError, json.JSONDecodeError):
        existing_products = []
        next_id = 1
    
    for i in range(count):
        theme = random.choice(THEMES)
        category = random.choice(CATEGORIES)
        is_free = random.choice([True, False, False])  # 33% șanse să fie gratuit
        
        product = {
            "id": next_id + i,
            "name": generate_product_name(theme),
            "category": category,
            "price": "GRATIS" if is_free else f"${random.choice([4.99, 5.99, 6.99, 7.99])}",
            "image": f"products/generated_{next_id + i}.png",
            "views": random.randint(100, 2000),
            "sales": random.randint(10, 150),
            "is_free": is_free,
            "generated_at": datetime.now().isoformat(),
            "theme": theme
        }
        
        products.append(product)
    
    # Combină cu produsele existente
    all_products = existing_products + products
    
    # Scrie în products_data.js
    js_content = f"var allProducts = {json.dumps(all_products, indent=2)};"
    
    with open("js/products_data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    
    return products

def main():
    print(f"🎨 Generare {PRODUCT_COUNT} produse noi...")
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    products = generate_products(PRODUCT_COUNT)
    
    print(f"\n✅ Generat {len(products)} produse noi în js/products_data.js")
    print("\n📦 Produse create:")
    for p in products:
        print(f"  - {p['name']} ({p['category']}) - {p['price']}")
    
    print("\n" + "=" * 50)
    print("🚀 Următorii pași:")
    print("  1. Rulează sync_products_now.py pentru a sincroniza cu Printful")
    print("  2. Deploy pe Netlify pentru a actualiza site-ul")
    print("=" * 50)

if __name__ == "__main__":
    main()
