"""
Script for automatic image generation using AI (Pollinations.ai)
and automatic population of the site with new products.
Integrates user suggestions from data/suggestions.txt
"""

import os
import json
import requests
import random
from datetime import datetime
from pathlib import Path

# Configuration
GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY', '')
PRODUCT_COUNT = int(os.getenv('PRODUCT_COUNT', '5'))
SUGGESTIONS_FILE = "data/suggestions.txt"

# Default themes for products
PRODUCT_THEMES = [
    {
        "name": "Space Explorer Dog",
        "category": "Coloring",
        "prompt": "A cute cartoon dog astronaut floating in colorful space with stars, planets, and a rocket. Simple black and white line art perfect for children's coloring book. Clean lines, no shading, white background.",
        "price": 4.99
    },
    {
        "name": "Underwater Mermaid Adventure",
        "category": "Stories",
        "prompt": "A friendly cartoon mermaid swimming with colorful fish and sea creatures. Simple black and white line art for children's coloring. Clean outlines, no shading, white background.",
        "price": 5.99
    },
    {
        "name": "Dinosaur Park Fun",
        "category": "Games",
        "prompt": "A happy cartoon T-Rex dinosaur playing in a prehistoric jungle with palm trees and volcanoes. Simple line art for kids coloring book. Bold outlines, no shading, white background.",
        "price": 4.99
    },
    {
        "name": "Magic Unicorn Rainbow",
        "category": "Coloring",
        "prompt": "A magical cartoon unicorn with flowing mane standing under a rainbow with clouds and stars. Simple black and white line art for children. Clean lines, no shading, white background.",
        "price": 4.99
    },
    {
        "name": "Robot Factory Adventure",
        "category": "Worksheets",
        "prompt": "A friendly cartoon robot with gears, buttons and antenna in a futuristic factory. Simple line art for kids coloring. Bold outlines, no shading, white background.",
        "price": 6.99
    }
]

def read_suggestions():
    """Reads keywords from suggestions from Railway API and local file."""
    suggestions_data = ""
    
    # 1. Try to fetch from Railway (Central Server)
    try:
        response = requests.get("https://web-production-b215.up.railway.app/api/admin/suggestions/text", timeout=10)
        if response.status_code == 200:
            suggestions_data = response.text
    except Exception as e:
        print(f"⚠️ Could not fetch suggestions from Railway: {e}")

    # 2. Try to read from local file as fallback/additional
    if os.path.exists(SUGGESTIONS_FILE):
        try:
            with open(SUGGESTIONS_FILE, "r") as f:
                suggestions_data += "\n" + f.read()
        except:
            pass

    if not suggestions_data.strip():
        return []

    try:
        content = suggestions_data.lower()
        # Parse the structured format: Name | Category | Suggestion
        keywords = []
        for line in content.split('\n'):
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    suggestion_text = parts[2].strip()
                    if suggestion_text:
                        keywords.append(suggestion_text)
            elif line.strip():
                keywords.append(line.strip())
        
        suggested_themes = []
        for kw in keywords:
            # Create a dynamic theme based on the keyword
            suggested_themes.append({
                "name": f"Magic {kw.title()[:20]}",
                "category": random.choice(["Coloring", "Stories", "Games"]),
                "prompt": f"A cute cartoon {kw} in a magical setting. Simple black and white line art for children's coloring book. Clean lines, no shading, white background.",
                "price": random.choice([4.99, 5.99, 6.99])
            })
        return suggested_themes
    except Exception as e:
        print(f"⚠️ Error parsing suggestions: {e}")
        return []

def generate_real_ai_image(product_id, theme_name, prompt):
    """
    Generates a real AI image using Pollinations.ai (Flux model)
    """
    print(f"🎨 Generating AI image for: {theme_name}...")
    
    # Add quality and style details
    full_prompt = f"{prompt}, high quality, children book style, vibrant, detailed, 8k"
    encoded_prompt = requests.utils.quote(full_prompt)
    
    # Construct URL with random seed for variation
    seed = random.randint(1, 999999)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&seed={seed}&nologo=true&model=flux"
    
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"❌ AI Image Generation Error: {e}")
        return None

def save_product_image(product_id, theme_name, prompt, output_dir="assets/images/products"):
    """Saves the generated product image (AI or placeholder)"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    filename = f"{output_dir}/product_{product_id}.jpg"
    
    image_content = generate_real_ai_image(product_id, theme_name, prompt)
    
    if image_content:
        with open(filename, 'wb') as f:
            f.write(image_content)
    else:
        # SVG Fallback
        svg_content = f'''<svg width="800" height="800" xmlns="http://www.w3.org/2000/svg">
            <rect width="800" height="800" fill="#f0f0f0"/>
            <text x="400" y="400" font-family="Arial" font-size="40" fill="#666" text-anchor="middle">
                {theme_name}
            </text>
        </svg>'''
        filename = f"{output_dir}/product_{product_id}.svg"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
    
    return filename

def load_existing_products():
    """Loads existing products from js/products_data.js"""
    try:
        if os.path.exists("js/products_data.js"):
            with open("js/products_data.js", "r", encoding="utf-8") as f:
                content = f.read()
                json_str = content.replace("var allProducts = ", "").rstrip(";").strip()
                if json_str:
                    return json.loads(json_str)
    except Exception as e:
        print(f"⚠️ Error loading products: {e}")
    return []

def generate_new_products(count):
    """Generates new products using suggestions and default themes"""
    existing_products = load_existing_products()
    next_id = max([p.get('id', 0) for p in existing_products], default=0) + 1
    
    suggestions = read_suggestions()
    # Combine suggestions with default themes, prioritizing suggestions
    available_themes = suggestions + PRODUCT_THEMES
    
    new_products = []
    
    for i in range(count):
        theme = available_themes[i % len(available_themes)]
        product_id = next_id + i
        
        image_path = save_product_image(product_id, theme['name'], theme['prompt'])
        
        is_free = random.random() < 0.2
        
        product = {
            "id": product_id,
            "name": f"{theme['name']} #{product_id}",
            "category": theme['category'],
            "price": "FREE" if is_free else f"£{theme['price']}",
            "image": image_path,
            "views": random.randint(10, 100),
            "sales": random.randint(1, 10) if not is_free else 0,
            "is_free": is_free,
            "generated_at": datetime.now().isoformat(),
            "theme": theme['name']
        }
        
        new_products.append(product)
    
    return existing_products + new_products

def save_products_to_js(products):
    """Updates the JS data file"""
    js_content = f"var allProducts = {json.dumps(products, indent=2)};"
    Path("js").mkdir(exist_ok=True)
    with open("js/products_data.js", "w", encoding="utf-8") as f:
        f.write(js_content)

def update_statistics(products):
    """Updates global site statistics"""
    stats = {
        "total_products": len(products),
        "total_views": sum(p.get('views', 0) for p in products),
        "total_sales": sum(p.get('sales', 0) for p in products),
        "last_updated": datetime.now().isoformat()
    }
    with open("site_statistics.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    return stats

def main():
    print("=" * 70)
    print("🎨 AUTOMATIC PRODUCT GENERATION - KIDS DIGITAL HUB")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_products = generate_new_products(PRODUCT_COUNT)
    save_products_to_js(all_products)
    update_statistics(all_products)
    
    print("\n✅ GENERATION COMPLETE!")
    print(f"📦 Total products: {len(all_products)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
