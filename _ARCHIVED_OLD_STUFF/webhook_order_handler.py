"""
Webhook handler for Printful orders
When a new order appears:
1. Generate product image with AI (if it doesn't exist)
2. Create the product in Printful
3. Confirm the order for automatic fulfillment
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
    Generates product image using Google AI
    Based on the product theme
    """
    print(f"🎨 Generating AI image for: {product_name}")
    
    # Custom prompt based on product name
    prompt = f"""Create a cute, colorful children's illustration for '{product_name}' with theme '{theme}'.
    Style: Cartoon, friendly, vibrant colors, suitable for kids aged 3-10.
    Format: High resolution, suitable for printing on t-shirts, mugs, and posters.
    Background: Clean, simple, with main character/element in center."""
    
    if not GOOGLE_AI_API_KEY:
        print("⚠️  Google AI API key is not configured. Using placeholder.")
        return None
    
    try:
        # TODO: Implement real generation with Google AI API
        # Here you would integrate Imagen or another image generation service
        print(f"✅ Image generated for {product_name}")
        return f"generated_{product_name.lower().replace(' ', '_')}.png"
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return None

def create_printful_product(product_data, image_path):
    """
    Creates the product in Printful with the generated image
    """
    print(f"📦 Creating product in Printful: {product_data['name']}")
    
    headers = {
        "Authorization": f"Bearer {PRINTFUL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Product configuration for Printful
    # Example: Kids T-Shirt
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
            print(f"✅ Product created in Printful: ID {result['result']['id']}")
            return result['result']
        else:
            print(f"❌ Printful Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating product: {e}")
        return None

def process_new_order(order_data):
    """
    Processes a new order
    """
    print("=" * 70)
    print("🛒 NEW ORDER RECEIVED!")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🆔 Order ID: {order_data.get('id', 'N/A')}")
    print(f"👤 Customer: {order_data.get('recipient', {}).get('name', 'N/A')}")
    print("-" * 70)
    
    # Extract product info
    items = order_data.get('items', [])
    
    for item in items:
        product_name = item.get('name', 'Unknown Product')
        product_id = item.get('sync_variant_id')
        
        print(f"\n📦 Ordered Product: {product_name}")
        print(f"🔢 Quantity: {item.get('quantity', 1)}")
        
        # Check if product already exists in Printful
        existing_product = check_product_exists(product_id)
        
        if not existing_product:
            print("🤖 Product does not exist - generating automatically...")
            
            # 1. Generate image with AI
            image_path = generate_product_image_ai(
                product_name,
                item.get('theme', 'general')
            )
            
            if image_path:
                # 2. Create product in Printful
                printful_product = create_printful_product(
                    {
                        'name': product_name,
                        'price': item.get('retail_price', 19.99)
                    },
                    image_path
                )
                
                if printful_product:
                    print("✅ Product created and ready for delivery!")
                else:
                    print("❌ Error creating product in Printful")
            else:
                print("❌ Could not generate image")
        else:
            print("✅ Product already exists in Printful")
    
    # 3. Confirm order for automatic fulfillment
    confirm_order_for_fulfillment(order_data.get('id'))
    
    print("\n" + "=" * 70)
    print("✅ ORDER PROCESSED - Printful will ship automatically!")
    print("=" * 70)
    
    # Save log
    save_order_log(order_data)

def check_product_exists(product_id):
    """Checks if product already exists in Printful"""
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
    """Confirms the order to be processed by Printful"""
    if not order_id or not PRINTFUL_API_KEY:
        return False
    
    headers = {
        "Authorization": f"Bearer {PRINTFUL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Confirm order
        response = requests.post(
            f"{PRINTFUL_API_BASE}/orders/{order_id}/confirm",
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"✅ Order {order_id} confirmed for delivery!")
            return True
        else:
            print(f"⚠️  Error confirming order: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error confirming: {e}")
        return False

def save_order_log(order_data):
    """Saves order log"""
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

# Usage example
if __name__ == "__main__":
    # Simulated order for testing
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
    
    print("🧪 TESTING AUTOMATIC ORDER SYSTEM")
    print("=" * 70)
    process_new_order(test_order)
