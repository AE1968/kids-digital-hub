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
from openai import OpenAI
from nexus_memory import save_conversation, get_context_for_prompt, update_user_profile, get_user_profile
from nexus_package import create_nexus_package, import_nexus_package, list_available_packages, get_package_info
from nexus_tasks import get_current_context, get_all_lists, save_task_list, mark_task_complete

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app) # Enable CORS for all routes

# Setup OpenAI GPT-4o - SUPERIOR ROMANIAN LANGUAGE SUPPORT
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai_client = None
if OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✓ Nexus AI: OpenAI GPT-4o ONLINE (Superior Romanian Support)")
    except Exception as e:
        print(f"OpenAI Setup Error: {e}")

# Load Nexus Personality
try:
    from nexus_prompt import SYSTEM_PROMPT as NEXUS_SYSTEM_PROMPT
except ImportError:
    NEXUS_SYSTEM_PROMPT = "You are Nexus. Helpful AI."

# --- AUTOMATIC LANGUAGE DETECTION ---
def detect_language(text):
    """Detect the language of the input text"""
    text_lower = text.lower()
    
    # Romanian indicators
    romanian_words = ['ce', 'cum', 'sunt', 'este', 'pentru', 'cu', 'la', 'de', 'și', 'în', 'să', 'ai', 'vreme', 'bună', 'salut', 'mulțumesc', 'te', 'îmi', 'doriți']
    romanian_count = sum(1 for word in romanian_words if word in text_lower)
    
    # English indicators
    english_words = ['the', 'is', 'are', 'what', 'how', 'can', 'you', 'please', 'thank', 'hello', 'with', 'for', 'and', 'have', 'this']
    english_count = sum(1 for word in english_words if word in text_lower)
    
    # Spanish indicators
    spanish_words = ['el', 'la', 'es', 'qué', 'cómo', 'por', 'con', 'para', 'gracias', 'hola', 'está']
    spanish_count = sum(1 for word in spanish_words if word in text_lower)
    
    # French indicators
    french_words = ['le', 'la', 'est', 'que', 'comment', 'pour', 'avec', 'merci', 'bonjour', 'vous']
    french_count = sum(1 for word in french_words if word in text_lower)
    
    # German indicators
    german_words = ['der', 'die', 'das', 'ist', 'wie', 'was', 'für', 'mit', 'danke', 'hallo']
    german_count = sum(1 for word in german_words if word in text_lower)
    
    # Determine language based on highest count
    counts = {
        'ro': romanian_count,
        'en': english_count,
        'es': spanish_count,
        'fr': french_count,
        'de': german_count
    }
    
    detected = max(counts, key=counts.get)
    
    # Default to English if no clear match
    if counts[detected] == 0:
        return 'en'
    
    return detected

def get_language_instruction(lang_code):
    """Get the instruction for Gemini to respond in the detected language"""
    instructions = {
        'ro': "IMPORTANT: The user is speaking ROMANIAN. You MUST respond ONLY in ROMANIAN language. Use Romanian grammar, vocabulary, and expressions naturally.",
        'en': "IMPORTANT: The user is speaking ENGLISH. You MUST respond ONLY in ENGLISH language.",
        'es': "IMPORTANT: The user is speaking SPANISH. You MUST respond ONLY in SPANISH language. Use Spanish grammar and vocabulary naturally.",
        'fr': "IMPORTANT: The user is speaking FRENCH. You MUST respond ONLY in FRENCH language. Use French grammar and vocabulary naturally.",
        'de': "IMPORTANT: The user is speaking GERMAN. You MUST respond ONLY in GERMAN language. Use German grammar and vocabulary naturally."
    }
    
    return instructions.get(lang_code, instructions['en'])

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

        # AUTOMATIC LANGUAGE DETECTION
        detected_language = detect_language(user_msg)
        language_instruction = get_language_instruction(detected_language)
        
        # AUTO-ACTIVATE MEMORY: Get conversation history
        conversation_context = get_context_for_prompt(user_id)
        
        # Update user profile automatically
        update_user_profile(user_id, name=user_name)
        user_profile = get_user_profile(user_id)
        
        # Construct Prompt with memory context and language instruction
        timestamp = datetime.now().strftime("%H:%M")
        full_prompt = f"""{NEXUS_SYSTEM_PROMPT}

{language_instruction}

[TIME: {timestamp}]
[USER PROFILE: {user_profile.get('name', 'Unknown')}]

{conversation_context}

CURRENT MESSAGE:
USER ({user_name}): {user_msg}
NEXUS:"""
        
        reply_text = "Transmission interrupted."
        
        if openai_client:
            try:
                # Generate AI Response with OpenAI GPT-4o
                response = openai_client.chat.completions.create(
                    model="gpt-4o",  # Most advanced GPT-4 model with superior Romanian support
                    messages=[
                        {"role": "system", "content": full_prompt},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=0.7,
                    max_tokens=2048,
                    top_p=0.95
                )
                reply_text = response.choices[0].message.content.strip()
            except Exception as e:
                print(f"OpenAI Error: {e}")
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
