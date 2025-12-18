import os
import shutil
import json
import re

# Configurare
PROJECT_ROOT = r"C:\Users\adria\.gemini\antigravity\scratch\kids-digital-hub"
NEW_PRODUCTS_DIR = os.path.join(PROJECT_ROOT, 'Produse_Noi')
IMAGES_DIR = os.path.join(PROJECT_ROOT, "assets", "images")
JS_OUTPUT = os.path.join(PROJECT_ROOT, "js", "products_data.js")

def sync_products():
    """Sincronizare produse din Produse_Noi -> products_data.js"""
    
    structure = {
        "Free": ["Coloring", "Games", "Stories", "Worksheets"],
        "Paid": ["Coloring", "Games", "Stories", "Worksheets"]
    }
    
    product_list = []
    p_id = 1
    
    for p_type, categories in structure.items():
        for cat in categories:
            source_path = os.path.join(NEW_PRODUCTS_DIR, p_type, cat)
            if not os.path.exists(source_path):
                continue
            
            # Scanare fisiere
            for fname in os.listdir(source_path):
                if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # 1. Copiaza in assets/images
                    src_file = os.path.join(source_path, fname)
                    dst_file = os.path.join(IMAGES_DIR, fname)
                    if not os.path.exists(dst_file):
                        shutil.copy2(src_file, dst_file)
                        print(f"Copiat: {fname}")
                    
                    # 2. Creaza obiect produs
                    clean_name = fname.replace("_", " ").replace(".jpg", "").replace(".png", "").replace(".jpeg", "")
                    # Sterge timestamp din nume
                    clean_name = re.sub(r'\d+$', '', clean_name).strip()
                    
                    price_label = "GRATIS" if p_type == "Free" else "$4.99"
                    
                    prod = {
                        "id": p_id,
                        "name": clean_name,
                        "category": cat,
                        "price": price_label,
                        "image": fname,
                        "views": 0,
                        "sales": 0,
                        "is_free": (p_type == "Free")
                    }
                    product_list.append(prod)
                    p_id += 1
    
    # Scrie in JS
    js_content = f"var allProducts = {json.dumps(product_list, indent=2)};"
    
    with open(JS_OUTPUT, "w", encoding="utf-8") as f:
        f.write(js_content)
    
    print(f"\n✅ Sincronizat {len(product_list)} produse in {JS_OUTPUT}")
    return len(product_list)

if __name__ == "__main__":
    count = sync_products()
    if count == 0:
        print("\n⚠️ ATENȚIE: Nu s-au găsit produse în folderele Produse_Noi!")
        print("Verifică că ai imagini în:")
        print("  - Produse_Noi/Free/Coloring")
        print("  - Produse_Noi/Free/Games")
        print("  - Produse_Noi/Paid/...")
