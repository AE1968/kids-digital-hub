import json

# Produse demo folosind imaginile existente
demo_products = [
    {
        "id": 1,
        "name": "Santa's Magic Workshop",
        "category": "Coloring",
        "price": "GRATIS",
        "image": "seasonal/winter-santa-lapland.png",
        "views": 1234,
        "sales": 89,
        "is_free": True
    },
    {
        "id": 2,
        "name": "Space Explorer Adventure",
        "category": "Games",
        "price": "$4.99",
        "image": "products/space_dog.png",
        "views": 987,
        "sales": 67,
        "is_free": False
    },
    {
        "id": 3,
        "name": "The Friendly Dragon",
        "category": "Stories",
        "price": "$4.99",
        "image": "products/story_dino.png",
        "views": 1456,
        "sales": 102,
        "is_free": False
    },
    {
        "id": 4,
        "name": "Unicorn Dreams",
        "category": "Coloring",
        "price": "GRATIS",
        "image": "products/unicorn.png",
        "views": 823,
        "sales": 45,
        "is_free": True
    },
    {
        "id": 5,
        "name": "Dino Safari Adventure",
        "category": "Games",
        "price": "$4.99",
        "image": "products/dino_safari.png",
        "views": 654,
        "sales": 34,
        "is_free": False
    },
    {
        "id": 6,
        "name": "Mermaid Tales",
        "category": "Stories",
        "price": "$4.99",
        "image": "products/story_mermaid.png",
        "views": 912,
        "sales": 56,
        "is_free": False
    },
    {
        "id": 7,
        "name": "Robot Builder",
        "category": "Games",
        "price": "GRATIS",
        "image": "products/robot.png",
        "views": 567,
        "sales": 23,
        "is_free": True
    },
    {
        "id": 8,
        "name": "Ocean Friends",
        "category": "Coloring",
        "price": "$4.99",
        "image": "products/octopus.png",
        "views": 789,
        "sales": 41,
        "is_free": False
    },
    {
        "id": 9,
        "name": "Moon Adventure Story",
        "category": "Stories",
        "price": "GRATIS",
        "image": "products/story_moon.png",
        "views": 445,
        "sales": 19,
        "is_free": True
    },
    {
        "id": 10,
        "name": "Variety Activity Pack",
        "category": "Worksheets",
        "price": "$4.99",
        "image": "products/pack_variety.png",
        "views": 334,
        "sales": 15,
        "is_free": False
    }
]

# Scrie in products_data.js
js_content = f"var allProducts = {json.dumps(demo_products, indent=2)};"

with open("js/products_data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"✅ Generat {len(demo_products)} produse demo în js/products_data.js")
print("\nProduse create:")
for p in demo_products:
    print(f"  - {p['name']} ({p['category']}) - {p['price']}")
