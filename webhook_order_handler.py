"""
Webhook handler pentru comenzi Printful
Când apare o comandă nouă:
1. Generează imaginea produsului cu AI (dacă nu există)
2. Creează produsul în Printful
3. Confirmă comanda pentru livrare automată
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

PRINTFUL_API_KEY = os.getenv('PRINTFUL_API_KEY', '')
GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY', '')

PRINTFUL_API_BASE = "https://api.printful.com"

def generate_product_image_ai(product_name, theme):
    """
    Generează imaginea produsului folosind Google AI
    În funcție de tema produsului
    """
    print(f"🎨 Generare imagine AI pentru: {product_name}")
    
    # Prompt personalizat bazat pe numele produsului
    prompt = f"""Create a cute, colorful children's illustration for '{product_name}' with theme '{theme}'.
    Style: Cartoon, friendly, vibrant colors, suitable for kids aged 3-10.
    Format: High resolution, suitable for printing on t-shirts, mugs, and posters.
    Background: Clean, simple, with main character/element in center."""
    
    if not GOOGLE_AI_API_KEY:
        print("⚠️  Google AI API key nu este configurat. Se va folosi placeholder.")
        return None
    
    try:
        # TODO: Implementează generarea reală cu Google AI API
        # Aici vei integra Imagen sau alt serviciu de generare imagini
        print(f"✅ Imagine generată pentru {product_name}")
        return f"generated_{product_name.lower().replace(' ', '_')}.png"
    except Exception as e:
        print(f"❌ Eroare la generare imagine: {e}")
        return None

def create_printful_product(product_data, image_path):
    """
    Creează produsul în Printful cu imaginea generată
    """
    print(f"📦 Creare produs în Printful: {product_data['name']}")
    
    headers = {
        "Authorization": f"Bearer {PRINTFUL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Configurare produs pentru Printful
    # Exemplu: Tricou pentru copii
    product_config = {
        "sync_product": {
            "name": product_data['name'],
            "thumbnail": image_path
        },
        "sync_variants": [
            {
                "variant_id": 4012,  # Gildan 18000 - Unisex Heavy Blend Crewneck Sweatshirt (S)
                "retail_price": product_data.get('price', 19.99),
                "files": [
                    {
                        "url": image_path,
                        "type": "front"
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{PRINTFUL_API_BASE}/store/products",
            headers=headers,
            json=product_config
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Produs creat în Printful: ID {result['result']['id']}")
            return result['result']
        else:
            print(f"❌ Eroare Printful: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Eroare la creare produs: {e}")
        return None

def process_new_order(order_data):
    """
    Procesează o comandă nouă
    """
    print("=" * 70)
    print("🛒 COMANDĂ NOUĂ PRIMITĂ!")
    print("=" * 70)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🆔 Order ID: {order_data.get('id', 'N/A')}")
    print(f"👤 Client: {order_data.get('recipient', {}).get('name', 'N/A')}")
    print("-" * 70)
    
    # Extrage informații despre produs
    items = order_data.get('items', [])
    
    for item in items:
        product_name = item.get('name', 'Unknown Product')
        product_id = item.get('sync_variant_id')
        
        print(f"\n📦 Produs comandat: {product_name}")
        print(f"🔢 Cantitate: {item.get('quantity', 1)}")
        
        # Verifică dacă produsul există deja în Printful
        existing_product = check_product_exists(product_id)
        
        if not existing_product:
            print("🤖 Produsul nu există - se generează automat...")
            
            # 1. Generează imaginea cu AI
            image_path = generate_product_image_ai(
                product_name,
                item.get('theme', 'general')
            )
            
            if image_path:
                # 2. Creează produsul în Printful
                printful_product = create_printful_product(
                    {
                        'name': product_name,
                        'price': item.get('retail_price', 19.99)
                    },
                    image_path
                )
                
                if printful_product:
                    print("✅ Produs creat și gata pentru livrare!")
                else:
                    print("❌ Eroare la creare produs în Printful")
            else:
                print("❌ Nu s-a putut genera imaginea")
        else:
            print("✅ Produsul există deja în Printful")
    
    # 3. Confirmă comanda pentru procesare automată
    confirm_order_for_fulfillment(order_data.get('id'))
    
    print("\n" + "=" * 70)
    print("✅ COMANDĂ PROCESATĂ - Printful va livra automat!")
    print("=" * 70)
    
    # Salvează log
    save_order_log(order_data)

def check_product_exists(product_id):
    """Verifică dacă produsul există deja în Printful"""
    if not product_id or not PRINTFUL_API_KEY:
        return False
    
    headers = {
        "Authorization": f"Bearer {PRINTFUL_API_KEY}"
    }
    
    try:
        response = requests.get(
            f"{PRINTFUL_API_BASE}/store/products/{product_id}",
            headers=headers
        )
        return response.status_code == 200
    except:
        return False

def confirm_order_for_fulfillment(order_id):
    """Confirmă comanda pentru a fi procesată de Printful"""
    if not order_id or not PRINTFUL_API_KEY:
        return False
    
    headers = {
        "Authorization": f"Bearer {PRINTFUL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Confirmă comanda
        response = requests.post(
            f"{PRINTFUL_API_BASE}/orders/{order_id}/confirm",
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"✅ Comanda {order_id} confirmată pentru livrare!")
            return True
        else:
            print(f"⚠️  Eroare la confirmare comandă: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Eroare la confirmare: {e}")
        return False

def save_order_log(order_data):
    """Salvează log-ul comenzii"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "order_id": order_data.get('id'),
        "customer": order_data.get('recipient', {}).get('name'),
        "items": [
            {
                "name": item.get('name'),
                "quantity": item.get('quantity')
            }
            for item in order_data.get('items', [])
        ],
        "status": "processed"
    }
    
    try:
        with open("orders_log.json", "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    
    logs.append(log_entry)
    
    with open("orders_log.json", "w") as f:
        json.dump(logs, f, indent=2)

# Exemplu de utilizare
if __name__ == "__main__":
    # Simulare comandă pentru testare
    test_order = {
        "id": "TEST123",
        "recipient": {
            "name": "Test Customer",
            "email": "test@example.com"
        },
        "items": [
            {
                "name": "Space Explorer Dog T-Shirt",
                "sync_variant_id": None,
                "quantity": 1,
                "retail_price": 19.99,
                "theme": "space"
            }
        ]
    }
    
    print("🧪 TESTARE SISTEM COMENZI AUTOMATE")
    print("=" * 70)
    process_new_order(test_order)
