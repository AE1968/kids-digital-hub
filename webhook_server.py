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

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app) # Enable CORS for all routes

# ... (rest of the file) ...

@app.route('/api/products', methods=['GET'])
def api_get_products():
    """Returns the list of generated products for the frontend"""
    try:
        if os.path.exists('data/products.json'):
            with open('data/products.json', 'r') as f:
                return jsonify(json.load(f))
        return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Simple in-memory rate limiting
from collections import defaultdict
import time

request_history = defaultdict(list)
RATE_LIMIT_DURATION = 60 # seconds
RATE_LIMIT_MAX_REQUESTS = 5 # max requests per minute per IP

@app.before_request
def rate_limit():
    ip = request.remote_addr
    now = time.time()
    
    # List of paths that are NOT rate limited (monitoring, static, webhooks)
    excluded_paths = ['/health', '/api/ping', '/api/uptime/detailed', '/webhook/', '/static/']
    if any(request.path.startswith(p) for p in excluded_paths):
        return

    # Filter out requests older than the duration
    request_history[ip] = [req_time for req_time in request_history[ip] if now - req_time < RATE_LIMIT_DURATION]
    
    # Check if limit exceeded
    if len(request_history[ip]) >= RATE_LIMIT_MAX_REQUESTS:
        return jsonify({
            'status': 'error',
            'message': 'Rate limit exceeded for health safety. Please try again later.'
        }), 429
        
    # Add current request
    request_history[ip].append(now)

# Configuration
# Dependencies: pillow, flask-cors, google-generativeai, requests
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-secret-key-change-this')
PORT = int(os.getenv('PORT', 8080))
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '') # For Gemini AI if needed

# Nexus AI Dashboard HTML
NEXUS_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <title>NEXUS CORE | AI SYSTEM</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --neon-cyan: #00f3ff;
            --neon-purple: #bc13fe;
            --matrix-green: #00ff41;
            --deep-black: #050505;
            --hud-bg: rgba(10, 20, 30, 0.85);
        }
        body {
            background-color: var(--deep-black);
            color: var(--neon-cyan);
            font-family: 'Rajdhani', sans-serif;
            margin: 0;
            overflow: hidden; /* App-like feel */
            height: 100vh;
            display: flex;
            flex-direction: column;
            background-image: 
                radial-gradient(circle at 50% 50%, rgba(0, 243, 255, 0.1) 0%, transparent 50%),
                linear-gradient(0deg, rgba(0,0,0,0.9) 0%, rgba(0,20,30,1) 100%);
        }
        
        /* --- VISUALIZATION CORE --- */
        .visor-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 1;
        }

        .robot-head {
            width: 300px;
            height: 350px;
            position: relative;
            filter: drop-shadow(0 0 20px var(--neon-cyan));
            animation: float 6s ease-in-out infinite;
        }

        .brain-core {
            position: absolute;
            top: 50px;
            left: 50px;
            width: 200px;
            height: 180px;
            background: radial-gradient(circle, var(--neon-purple), transparent);
            border-radius: 50%;
            opacity: 0.6;
            animation: pulse-brain 3s infinite alternate;
            mix-blend-mode: screen;
        }

        .circuit-lines {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 2px solid var(--neon-cyan);
            border-radius: 40px 40px 100px 100px;
            box-shadow: inset 0 0 30px var(--neon-cyan);
            background: rgba(0, 243, 255, 0.05);
            clip-path: polygon(10% 0, 90% 0, 100% 20%, 100% 80%, 80% 100%, 20% 100%, 0 80%, 0 20%);
        }
        
        .eye-scanner {
            position: absolute;
            top: 40%;
            left: 10%;
            width: 80%;
            height: 4px;
            background: var(--matrix-green);
            box-shadow: 0 0 10px var(--matrix-green);
            animation: scan 2s linear infinite;
            opacity: 0.7;
        }

        @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-20px); } 100% { transform: translateY(0px); } }
        @keyframes pulse-brain { 0% { transform: scale(0.9); opacity: 0.3; } 100% { transform: scale(1.1); opacity: 0.8; box-shadow: 0 0 50px var(--neon-purple); } }
        @keyframes scan { 0% { top: 30%; opacity: 0; } 50% { opacity: 1; } 100% { top: 70%; opacity: 0; } }

        /* --- HUD ELEMENTS --- */
        .hud-top {
            position: absolute;
            top: 20px;
            width: 100%;
            text-align: center;
        }
        .nexus-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            letter-spacing: 5px;
            text-shadow: 0 0 20px var(--neon-cyan);
            margin: 0;
        }
        .status-badge {
            background: rgba(0,0,0,0.5);
            border: 1px solid var(--matrix-green);
            color: var(--matrix-green);
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        /* --- COMMUNICATION TAB --- */
        .comm-panel {
            height: 250px;
            background: var(--hud-bg);
            border-top: 2px solid var(--neon-purple);
            box-shadow: 0 -10px 50px rgba(188, 19, 254, 0.2);
            padding: 20px;
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(10px);
            z-index: 10;
        }
        
        .comm-header {
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--neon-purple);
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
            border-bottom: 1px solid rgba(188, 19, 254, 0.3);
            padding-bottom: 5px;
        }

        .chat-log {
            flex: 1;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            color: #ddd;
            margin-bottom: 10px;
        }
        
        .chat-entry {
            margin-bottom: 5px;
            opacity: 0;
            animation: fadeIn 0.3s forwards;
        }
        .chat-nexus { color: var(--neon-cyan); }
        .chat-user { color: var(--matrix-green); text-align: right; }

        .input-area {
            display: flex;
            gap: 10px;
        }
        
        .neural-input {
            flex: 1;
            background: rgba(0,0,0,0.5);
            border: 1px solid var(--neon-cyan);
            color: white;
            padding: 12px;
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.1rem;
            border-radius: 5px;
            outline: none;
        }
        
        .neural-input:focus { box-shadow: 0 0 15px rgba(0, 243, 255, 0.3); }

        .send-btn {
            background: var(--neon-purple);
            color: white;
            border: none;
            padding: 0 30px;
            font-family: 'Orbitron', sans-serif;
            cursor: pointer;
            clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
            transition: all 0.2s;
        }
        .send-btn:hover { transform: translateX(5px); box-shadow: -5px 0 15px var(--neon-purple); }

        .btn-exit {
            position: absolute;
            top: 20px;
            left: 20px;
            background: transparent;
            border: 1px solid red;
            color: red;
            padding: 5px 10px;
            cursor: pointer;
        }

        @keyframes fadeIn { to { opacity: 1; } }
    </style>
</head>
<body>

    <button class="btn-exit" onclick="location.href='/admin'"> < BACK </button>

    <div class="hud-top">
        <h1 class="nexus-title">NEXUS CORE</h1>
        <span class="status-badge">SYSTEM OPTIMAL • CONNECTED</span>
    </div>

    <div class="visor-container">
        <!-- THE ROBOT BRAIN VISUALIZATION -->
        <div class="robot-head">
            <div class="circuit-lines"></div>
            <div class="brain-core"></div>
            <div class="eye-scanner"></div>
            
            <!-- SVG ICON OVERLAY -->
            <svg viewBox="0 0 100 100" style="position: absolute; top:0; left:0; width:100%; height:100%; opacity:0.3; fill:none; stroke:var(--neon-cyan); stroke-width:0.5;">
                <path d="M20,20 L80,20 L90,40 L90,80 L80,90 L20,90 L10,80 L10,40 Z" />
                <path d="M30,30 L70,30 M30,40 L70,40 M30,50 L70,50" stroke-dasharray="2,2" />
                <circle cx="50" cy="50" r="10" stroke="var(--neon-purple)" />
            </svg>
        </div>
        
        <div style="margin-top: 30px; font-family: 'Courier New'; color: var(--neon-cyan); opacity: 0.8;">
            >_ PROCESSING NEURAL STREAMS... <span id="stream-cursor">▋</span>
        </div>
    </div>

    <!-- COMMUNICATION TAB -->
    <div class="comm-panel">
        <div class="comm-header">
            <span>● NEURAL LINK ACTIVE</span>
            <span style="flex:1"></span>
            <span style="font-size:0.8em; opacity:0.6;">ENCRYPTION: QUANTUM-256</span>
        </div>
        
        <div class="chat-log" id="chatLog">
            <div class="chat-entry chat-nexus">[NEXUS]: Welcome, Adrian. I am online and listening.</div>
            <div class="chat-entry chat-nexus">[NEXUS]: Systems are functioning within normal parameters.</div>
        </div>
        
        <form class="input-area" onsubmit="sendNeuralMessage(event)">
            <input type="text" id="neuralMsg" class="neural-input" placeholder="Transmit direct command..." autocomplete="off">
            <button type="submit" class="send-btn">TRANSMIT</button>
        </form>
    </div>

    <script>
        // Blinking Cursor
        setInterval(() => {
            const c = document.getElementById('stream-cursor');
            c.style.opacity = c.style.opacity === '0' ? '1' : '0';
        }, 500);

        function sendNeuralMessage(e) {
            e.preventDefault();
            const input = document.getElementById('neuralMsg');
            const msg = input.value.trim();
            if (!msg) return;

            // Add User Message
            addLog(msg, 'user');
            input.value = '';

            // Simulate Nexus processing (In real version, fetch API)
            setTimeout(() => {
                const responses = [
                    "Command received. Processing...",
                    "Analyzing data streams...",
                    "Optimization protocols engaged.",
                    "I am monitoring the traffic flows.",
                    "The VIP Club is currently active."
                ];
                const reply = responses[Math.floor(Math.random() * responses.length)];
                addLog(reply, 'nexus');
            }, 800);
        }

        function addLog(text, sender) {
            const log = document.getElementById('chatLog');
            const div = document.createElement('div');
            div.className = `chat-entry chat-${sender}`;
            div.innerHTML = `[${sender.toUpperCase()}]: ${text}`;
            log.appendChild(div);
            log.scrollTop = log.scrollHeight;
        }
    </script>
</body>
</html>
"""

# Admin Dashboard HTML
ADMIN_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google" content="notranslate">
    <title>Kids Digital Hub - Admin Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Fredoka', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            font-size: 1.1em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .section {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        .status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        .status.active {
            background: #4CAF50;
            color: white;
        }
        .status.pending {
            background: #FF9800;
            color: white;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background: #f8f9fa;
            color: #667eea;
            font-weight: 600;
        }
        .btn {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }
        .btn:hover {
            background: #764ba2;
            transform: scale(1.05);
        }
        .emoji {
            font-size: 1.5em;
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Kids Digital Hub - Admin Dashboard</h1>
            <p class="subtitle">Automatic product generation & delivery system</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">📦 Total Orders</div>
                <div class="stat-number">{{ total_orders }}</div>
                <span class="status active">Active</span>
            </div>
            <div class="stat-card">
                <div class="stat-label">🎨 Generated Products</div>
                <div class="stat-number">{{ total_products }}</div>
                <span class="status active">AI Enabled</span>
            </div>
            <div class="stat-card">
                <div class="stat-label">💰 Total Sales</div>
                <div class="stat-number">£{{ total_revenue }}</div>
                <span class="status active">Live</span>
            </div>
            <div class="stat-card">
                <div class="stat-label">🚀 Server Status</div>
                <div class="stat-number">✓</div>
                <span class="status active">Online</span>
            </div>
        </div>

        <div class="section">
            <h2>📊 Recent Orders</h2>
            <table>
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer</th>
                        <th>Product</th>
                        <th>Status</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for order in recent_orders %}
                    <tr>
                        <td>{{ order.id }}</td>
                        <td>{{ order.customer }}</td>
                        <td>{{ order.product }}</td>
                        <td><span class="status {{ order.status_class }}">{{ order.status }}</span></td>
                        <td>{{ order.date }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>💡 Recent Suggestions & AI Requests</h2>
            <table>
                <thead>
                    <tr>
                        <th>User</th>
                        <th>Type</th>
                        <th>Suggestion</th>
                        <th>Source Analysis</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {% for sugg in recent_suggestions %}
                    <tr>
                        <td>{{ sugg.name }}</td>
                        <td>{{ sugg.category }}</td>
                        <td>{{ sugg.suggestion }}</td>
                        <td><span class="status {{ sugg.source_class }}">{{ sugg.source_label }}</span></td>
                        <td>{{ sugg.timestamp }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>⚙️ System Configuration</h2>
            <p><strong>🔑 Printful API:</strong> <span class="status active">Configured</span></p>
            <p><strong>🤖 Google AI API:</strong> <span class="status active">Configured</span></p>
            <p><strong>🌐 Webhook URL:</strong> <code>{{ webhook_url }}</code></p>
            <p><strong>📅 Last Update:</strong> {{ last_update }}</p>
            <br>
            <br>
            <button class="btn" onclick="testWebhook()">🧪 Test Webhook</button>
            <button class="btn" onclick="generateProducts()">🎨 Generate New Products</button>
            <button class="btn" style="background:black; border: 2px solid #00ff41; color: #00ff41;" onclick="location.href='/admin/nexus'">🤖 ENTER NEXUS CORE</button>
        </div>
    </div>

    <script>
        function testWebhook() {
            alert('🧪 Testing webhook...');
            fetch('/api/test-webhook', { method: 'POST' })
                .then(r => r.json())
                .then(data => alert('✅ ' + data.message))
                .catch(e => alert('❌ Error: ' + e));
        }

        function generateProducts() {
            if(confirm('Generate 5 new products with AI?')) {
                alert('🎨 Generation in progress... Check back in a few minutes!');
                fetch('/api/generate-products', { method: 'POST' })
                    .then(r => r.json())
                    .then(data => alert('✅ ' + data.message))
                    .catch(e => alert('❌ Error: ' + e));
            }
        }

        // Auto-refresh every 30 seconds
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
"""

def verify_webhook_signature(request_data, signature):
    """Verifies Printful webhook signature"""
    computed = hmac.new(
        WEBHOOK_SECRET.encode(),
        request_data,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, computed)

@app.route('/')
def home():
    """Main page - redirects to admin"""
    return """
    <html>
    <head>
        <title>Kids Digital Hub - Webhook Server</title>
        <style>
            body {
                font-family: Arial;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
            }
            h1 { font-size: 3em; margin-bottom: 20px; }
            a {
                color: white;
                background: rgba(255,255,255,0.2);
                padding: 15px 30px;
                border-radius: 25px;
                text-decoration: none;
                font-size: 1.2em;
                transition: all 0.3s;
            }
            a:hover { background: rgba(255,255,255,0.3); }
        </style>
    </head>
    <body>
        <div>
            <h1>🎨 Kids Digital Hub</h1>
            <p>Webhook Server Active</p>
            <br><br>
            <a href="/admin">📊 Admin Dashboard</a>
        </div>
    </body>
    </html>
    """

@app.route('/admin/nexus')
def nexus_core():
    """Renders the Nexus AI Interface"""
    return render_template('nexus_core.html')

@app.route('/api/nexus/memory')
def get_nexus_memory():
    """Returns the core memory for the interface"""
    try:
        if os.path.exists('SYSTEM_CORE_MEMORY.json'):
            with open('SYSTEM_CORE_MEMORY.json', 'r') as f:
                return jsonify(json.load(f))
    except:
        pass
    return jsonify({"error": "Memory not found"})

@app.route('/admin')
def admin_dashboard():
    """Admin Dashboard"""
    # Load statistics
    try:
        with open('orders_log.json', 'r') as f:
            orders = json.load(f)
    except:
        orders = []
    
    try:
        with open('site_statistics.json', 'r') as f:
            stats = json.load(f)
    except:
        stats = {'total_products': 0, 'total_views': 0, 'total_sales': 0}
    
    # Prepare data for template
    recent_orders = []
    for order in orders[-10:]:  # Last 10 orders
        recent_orders.append({
            'id': order.get('order_id', 'N/A'),
            'customer': order.get('customer', 'N/A'),
            'product': order.get('items', [{}])[0].get('name', 'N/A'),
            'status': order.get('status', 'pending'),
            'status_class': 'active' if order.get('status') == 'processed' else 'pending',
            'date': order.get('timestamp', '')[:10]
        })
    
    # Load suggestions
    try:
        with open('data/suggestions_log.json', 'r') as f:
            suggestions_data = json.load(f)
    except:
        suggestions_data = []

    recent_suggestions = []
    for sugg in suggestions_data[:10]:
        recent_suggestions.append({
            'name': sugg.get('name', 'N/A'),
            'category': sugg.get('category', 'N/A'),
            'suggestion': sugg.get('suggestion', ''),
            'source_label': sugg.get('source_label', 'Guest'),
            'source_class': sugg.get('source_class', 'pending'),
            'timestamp': sugg.get('timestamp', '')[:16].replace('T', ' ')
        })

    return render_template_string(
        ADMIN_DASHBOARD,
        total_orders=len(orders),
        total_products=stats.get('total_products', 0),
        total_revenue=stats.get('total_sales', 0) * 7.5,
        recent_orders=reversed(recent_orders),
        recent_suggestions=recent_suggestions,
        webhook_url=request.host_url + 'webhook/order',
        last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/webhook/order', methods=['POST'])
def webhook_order():
    """Receives webhooks from Printful for new orders"""
    try:
        # Verify signature
        signature = request.headers.get('X-Printful-Signature', '')
        if WEBHOOK_SECRET != 'your-secret-key-change-this':
            if not verify_webhook_signature(request.data, signature):
                return jsonify({'error': 'Invalid signature'}), 403
        
        # Parse order data
        order_data = request.json
        
        print(f"📦 New order received: {order_data.get('id', 'N/A')}")
        
        # Process order automatically
        process_new_order(order_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Order processed successfully'
        }), 200
        
    except Exception as e:
        print(f"❌ Order processing error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/test-webhook', methods=['POST'])
def test_webhook():
    """Tests the webhook with a fake order"""
    test_order = {
        "id": f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "recipient": {
            "name": "Test Customer",
            "email": "test@example.com"
        },
        "items": [
            {
                "name": "Space Explorer Dog T-Shirt",
                "quantity": 1,
                "retail_price": 19.99,
                "theme": "space"
            }
        ]
    }
    
    process_new_order(test_order)
    
    return jsonify({
        'status': 'success',
        'message': 'Test order processed! Check logs.'
    })

@app.route('/api/generate-products', methods=['POST'])
def api_generate_products():
    """Manually triggers product generation"""
    try:
        import subprocess
        subprocess.run(['python', 'generate_ai_products.py'], check=True)
        return jsonify({
            'status': 'success',
            'message': '5 new products successfully generated!'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/suggestion', methods=['POST'])
def receive_suggestion():
    """Receives suggestions, analyzes user tier, and triggers AI for paid users."""
    try:
        data = request.json
        name = data.get('name', 'Anonymous')
        category = data.get('category', 'Other')
        suggestion = data.get('suggestion', '')
        role = data.get('role', 'guest')
        
        # Analyze Source
        source_label = 'Guest'
        source_class = 'pending' # Default check color
        
        if role in ['premium', 'gold', 'titan']:
            source_label = '✨ VIP'
            source_class = 'active' # Green/Special
        elif role in ['standard', 'monthly', 'subscriber']:
            source_label = '🛒 Subscriber'
            source_class = 'pending' # Orange
            
        # Log Logic
        log_entry = {
            'type': 'suggestion',
            'name': name,
            'category': category,
            'suggestion': suggestion,
            'role': role,
            'source_label': source_label,
            'source_class': source_class,
            'timestamp': datetime.now().isoformat(),
            'status': 'unread'
        }
        
        # Save to suggestions.txt for the AI to read (Legacy Support)
        os.makedirs('data', exist_ok=True)
        with open('data/suggestions.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{name} | {category} | {suggestion} | {source_label}")
            
        # Smart Trigger: If Paid User, Generate Automatically
        if role != 'guest':
            print(f"🚀 Triggering AI Generation for {source_label}: {name}")
            import subprocess
            # We run it in background effectively by not waiting or by just firing standard gen
            # For now, we trigger the standard batch. In future, we can pass args.
            try:
                subprocess.Popen(['python', 'generate_ai_products.py']) 
            except Exception as sub_e:
                print(f"AI Trigger Error: {sub_e}")

        
        # Also store in a JSON for the admin to view
        suggestions_log = []
        if os.path.exists('data/suggestions_log.json'):
            with open('data/suggestions_log.json', 'r') as f:
                suggestions_log = json.load(f)
        
        suggestions_log.insert(0, log_entry)
        with open('data/suggestions_log.json', 'w') as f:
            json.dump(suggestions_log[:100], f, indent=2)
            
        return jsonify({'status': 'success', 'message': 'Suggestion received!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def receive_contact():
    """Receives contact messages from the frontend."""
    try:
        data = request.json
        name = data.get('name', 'Anonymous')
        email = data.get('email', 'N/A')
        subject = data.get('subject', 'General Inquiry')
        message = data.get('message', '')
        user_lang = data.get('userLanguage', 'en')
        romanian_message = data.get('romanianMessage', '')
        
        log_entry = {
            'type': 'contact',
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'messageLang': user_lang,
            'romanianMessage': romanian_message,
            'timestamp': datetime.now().isoformat(),
            'status': 'unread'
        }
        
        # Store in contacts_log.json
        os.makedirs('data', exist_ok=True)
        contacts_log = []
        if os.path.exists('data/contacts_log.json'):
            with open('data/contacts_log.json', 'r') as f:
                contacts_log = json.load(f)
        
        contacts_log.insert(0, log_entry)
        with open('data/contacts_log.json', 'w') as f:
            json.dump(contacts_log[:100], f, indent=2)
            
        return jsonify({'status': 'success', 'message': 'Message received!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats/track', methods=['POST'])
def track_visit():
    """Tracks real visitor hits"""
    try:
        ip = request.remote_addr
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Load Stats
        if os.path.exists('site_statistics.json'):
            with open('site_statistics.json', 'r') as f:
                stats = json.load(f)
        else:
            stats = {'total_views': 0, 'daily_unique': {}, 'total_products': 0, 'total_sales': 0}
            
        # Update Total Views (Page Hits)
        stats['total_views'] = stats.get('total_views', 0) + 1
        
        # Update Daily Unique Visitors
        daily_data = stats.get('daily_unique', {})
        if today not in daily_data:
            daily_data[today] = []
        
        if ip not in daily_data[today]:
            daily_data[today].append(ip)
            
        # Clean up old days (keep last 7 days)
        keys = sorted(daily_data.keys())
        if len(keys) > 7:
            for k in keys[:-7]:
                del daily_data[k]
                
        stats['daily_unique'] = daily_data
        
        # Save
        with open('site_statistics.json', 'w') as f:
            json.dump(stats, f, indent=2)
            
        return jsonify({'status': 'tracked'})
    except:
        return jsonify({'status': 'error'}), 500

@app.route('/api/stats/view', methods=['GET'])
def get_stats():
    """Returns real stats"""
    if os.path.exists('site_statistics.json'):
        with open('site_statistics.json', 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'total_views': 0})

@app.route('/api/admin/messages', methods=['GET'])
def get_admin_messages():
    """Returns all suggestions and contact messages for the admin dashboard."""
    # (Existing code...)
    all_messages = []
    
    try:
        if os.path.exists('data/suggestions_log.json'):
            with open('data/suggestions_log.json', 'r') as f:
                all_messages.extend(json.load(f))
        
        if os.path.exists('data/contacts_log.json'):
            with open('data/contacts_log.json', 'r') as f:
                all_messages.extend(json.load(f))
        
        # Sort by timestamp
        all_messages.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify(all_messages)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/admin/suggestions/text', methods=['GET'])
def get_suggestions_text():
    """Returns the raw text of user suggestions for the AI generation scripts."""
    try:
        if os.path.exists('data/suggestions.txt'):
            with open('data/suggestions.txt', 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    except Exception as e:
        return str(e), 500

@app.route('/api/admin/message/read', methods=['POST'])
def mark_message_read():
    """Marks a message as read in the server logs."""
    try:
        data = request.json
        timestamp = data.get('timestamp')
        msg_type = data.get('type') # 'contact' or 'suggestion'
        
        file_path = f"data/{msg_type}s_log.json"
        if not os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': 'Log not found'}), 404
            
        with open(file_path, 'r') as f:
            logs = json.load(f)
            
        for log in logs:
            if log.get('timestamp') == timestamp:
                log['status'] = 'read'
                break
                
        with open(file_path, 'w') as f:
            json.dump(logs, f, indent=2)
            
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/admin/message/delete', methods=['POST'])
def delete_message():
    """Deletes a message from the server logs."""
    try:
        data = request.json
        timestamp = data.get('timestamp')
        msg_type = data.get('type')
        
        file_path = f"data/{msg_type}s_log.json"
        if not os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': 'Log not found'}), 404
            
        with open(file_path, 'r') as f:
            logs = json.load(f)
            
        logs = [log for log in logs if log.get('timestamp') != timestamp]
                
        with open(file_path, 'w') as f:
            json.dump(logs, f, indent=2)
            
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health')
def health():
    """Simple health check for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'kids-digital-hub-webhook'
    })

@app.route('/api/ping')
def ping():
    """Keep-alive endpoint"""
    return "pong"

@app.route('/api/uptime/detailed')
def uptime_detailed():
    """Detailed health check including partner services"""
    import requests
    results = {
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'partners': {},
        'internal': {}
    }
    
    # Check Partners
    partners = {
        'Netlify': 'https://www.kidsdigitalhub.com',
        'GoatCounter': 'https://adrian.goatcounter.com',
        'Cloudinary': 'https://cloudinary.com'
    }
    
    for name, url in partners.items():
        try:
            resp = requests.get(url, timeout=5)
            results['partners'][name] = 'online' if resp.status_code < 400 else f'error_{resp.status_code}'
        except:
            results['partners'][name] = 'unreachable'
            results['status'] = 'degraded'
            
    # Check Internal Storage
    paths_to_check = ['data/products.json', 'data/suggestions_log.json', 'site_statistics.json']
    for p in paths_to_check:
        results['internal'][p] = 'exists' if os.path.exists(p) else 'missing'
        
    return jsonify(results)

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 KIDS DIGITAL HUB - WEBHOOK SERVER")
    print("=" * 70)
    print(f"📡 Server running on port {PORT}")
    print(f"🌐 Admin Dashboard: http://localhost:{PORT}/admin")
    print(f"📦 Webhook URL: http://localhost:{PORT}/webhook/order")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
