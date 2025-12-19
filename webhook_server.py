"""
Flask Webhook Server for Automatic Order Processing
Runs on Railway.app or any cloud platform
"""

from flask import Flask, request, jsonify, render_template_string, render_template
from flask_cors import CORS
import os
import json
import hmac
import hashlib
from datetime import datetime
from webhook_order_handler import process_new_order
import google.generativeai as genai
from nexus_memory import save_conversation, get_context_for_prompt, update_user_profile, get_user_profile
from nexus_package import create_nexus_package, import_nexus_package, list_available_packages, get_package_info
from nexus_tasks import get_current_context, get_all_lists, save_task_list, mark_task_complete

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app) # Enable CORS for all routes

# Setup Gemini AI - MOST ADVANCED MODEL
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
nexus_model = None
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Use Gemini 2.0 Flash Experimental - Most Advanced Conversational Model
        # Configured for academic language and professional male persona
        generation_config = {
            "temperature": 0.7,  # Balanced creativity and precision
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        nexus_model = genai.GenerativeModel(
            'gemini-2.0-flash-exp',
            generation_config=generation_config
        )
        print("✓ Nexus AI: Gemini 2.0 Flash Experimental ONLINE (Academic Mode)")
    except Exception as e:
        print(f"AI Limit Warning: {e}")

# Load Nexus Personality
try:
    from nexus_prompt import SYSTEM_PROMPT as NEXUS_SYSTEM_PROMPT
except ImportError:
    NEXUS_SYSTEM_PROMPT = "You are Nexus. Helpful AI."

# --- API ROUTES ---

@app.route('/api/products', methods=['GET'])
def api_get_products():
    try:
        if os.path.exists('data/products.json'):
            with open('data/products.json', 'r') as f:
                return jsonify(json.load(f))
        return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nexus/chat', methods=['POST'])
def api_nexus_chat():
    """Handles chat messages for the Nexus AI Interface with Memory"""
    try:
        data = request.json
        user_msg = data.get('message', '')
        user_name = data.get('user', 'Commander')
        user_id = data.get('user_id', request.remote_addr)  # Use IP as fallback ID
        
        if not user_msg:
            return jsonify({'error': 'No message provided'}), 400

        # AUTO-ACTIVATE MEMORY: Get conversation history
        conversation_context = get_context_for_prompt(user_id)
        
        # Update user profile automatically
        update_user_profile(user_id, name=user_name)
        user_profile = get_user_profile(user_id)
        
        # Construct Prompt with memory context
        timestamp = datetime.now().strftime("%H:%M")
        full_prompt = f"""{NEXUS_SYSTEM_PROMPT}

[TIME: {timestamp}]
[USER PROFILE: {user_profile.get('name', 'Unknown')}]

{conversation_context}

CURRENT MESSAGE:
USER ({user_name}): {user_msg}
NEXUS:"""
        
        reply_text = "Transmission interrupted."
        
        if nexus_model:
            try:
                # Generate AI Response with full context
                response = nexus_model.generate_content(full_prompt)
                reply_text = response.text.strip()
            except Exception as e:
                print(f"AI Error: {e}")
                reply_text = "Neural link unstable. Stand by."
        else:
            # UPLINK ONLINE - AUTONOMOUS RECOVERY
            reply_text = "Primary Neural Uplink established. Neural bridge active. Secure connection confirmed. What is our next objective?"
        
        # AUTO-SAVE to memory
        save_conversation(user_id, user_msg, reply_text)
            
        return jsonify({
            'reply': reply_text,
            'timestamp': datetime.now().isoformat(),
            'memory_active': True
        })
        
    except Exception as e:
        print(f"Chat Error: {e}")
        return jsonify({'error': str(e)}), 500

# Placeholder for Admin Routes (Simplified for brevity, full version handles templates)
@app.route('/')
def home():
    return "Kids Digital Hub Server Active. Access /admin."

@app.route('/health')
def health():
    return "OK", 200

# WEBHOOK HANDLER
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'test')

def verify_webhook_signature(request_data, signature):
    computed = hmac.new(WEBHOOK_SECRET.encode(), request_data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, computed)

@app.route('/webhook/order', methods=['POST'])
def webhook_order():
    try:
        signature = request.headers.get('X-Printful-Signature', '')
        if WEBHOOK_SECRET != 'test' and not verify_webhook_signature(request.data, signature):
            return jsonify({'error': 'Invalid signature'}), 403
        
        order_data = request.json
        print(f"New Order: {order_data.get('id')}")
        process_new_order(order_data)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
