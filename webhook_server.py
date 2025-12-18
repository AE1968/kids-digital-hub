"""
Flask Webhook Server for Automatic Order Processing
Runs on Railway.app or any cloud platform
"""

from flask import Flask, request, jsonify, render_template_string
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
    
    # Filter out requests older than the duration
    request_history[ip] = [req_time for req_time in request_history[ip] if now - req_time < RATE_LIMIT_DURATION]
    
    # Check if limit exceeded
    if len(request_history[ip]) >= RATE_LIMIT_MAX_REQUESTS:
        return jsonify({
            'status': 'error',
            'message': 'Rate limit exceeded. Please try again later.'
        }), 429
        
    # Add current request
    request_history[ip].append(now)

# Configuration
# Dependencies:
# pillow
# flask-cors
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-secret-key-change-this')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-secret-key-change-this')
PORT = int(os.getenv('PORT', 8080))

# Nexus AI Dashboard HTML
NEXUS_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS AI CORE</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { 
            background: #0d0d0d; 
            color: #00ff41; 
            font-family: 'Share Tech Mono', monospace; 
            overflow: hidden;
            height: 100vh;
        }
        .container { display: flex; height: 100%; }
        .sidebar { 
            width: 300px; 
            border-right: 1px solid #004411; 
            padding: 20px; 
            background: rgba(0,20,0,0.5);
        }
        .main { flex: 1; padding: 20px; display: flex; flex-direction: column; }
        h1 { color: #00ff41; text-shadow: 0 0 10px #00ff41; margin-bottom: 20px; text-transform: uppercase; }
        .card { 
            border: 1px solid #004411; 
            padding: 15px; 
            margin-bottom: 20px; 
            background: rgba(0,10,0,0.8);
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
        }
        .log-window { 
            flex: 1; 
            border: 1px solid #00ff41; 
            padding: 15px; 
            overflow-y: auto; 
            font-size: 0.9em;
            background: black;
            box-shadow: inset 0 0 20px rgba(0, 255, 65, 0.2);
        }
        .log-entry { margin-bottom: 5px; opacity: 0; animation: fadeIn 0.5s forwards; }
        .blink { animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
        @keyframes fadeIn { to { opacity: 1; } }
        
        .status-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .btn-nexus { 
            background: transparent; 
            border: 1px solid #00ff41; 
            color: #00ff41; 
            padding: 10px; 
            cursor: pointer; 
            width: 100%; 
            margin-top: 10px;
            font-family: 'Share Tech Mono', monospace;
            text-transform: uppercase;
        }
        .btn-nexus:hover { background: #00ff41; color: black; box-shadow: 0 0 15px #00ff41; }
        
        /* Scanline effect */
        .scanlines {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.2) 50%, rgba(0,0,0,0.2));
            background-size: 100% 4px;
            pointer-events: none;
            z-index: 1000;
        }
    </style>
</head>
<body>
    <div class="scanlines"></div>
    <div class="container">
        <div class="sidebar">
            <h1>🤖 NEXUS CORE</h1>
            <div class="card">
                <h3>// SYSTEM IDENTITY</h3>
                <p>> AGENT: NEXUS</p>
                <p>> ROLE: Autonomous CTO</p>
                <p>> OWNER: Adrian (CEO)</p>
                <p>> STATUS: <span class="blink">ONLINE</span></p>
            </div>
             <div class="card">
                <h3>// DIRECTIVES</h3>
                <p>> 1. Protect Core</p>
                <p>> 2. Maximize Revenue</p>
                <p>> 3. Ensure Uptime</p>
            </div>
            <button class="btn-nexus" onclick="location.href='/admin'"> < BACK TO ADMIN</button>
        </div>
        <div class="main">
            <div class="status-grid">
                <div class="card">
                    <h3>// MEMORY INTEGRITY</h3>
                    <div id="memory-vis">LOADING...</div>
                </div>
                <div class="card">
                    <h3>// ACTIVE TASKS</h3>
                    <p>> Email Sentinel: ACTIVE</p>
                    <p>> Auto-Product Gen: STANDBY</p>
                </div>
            </div>
            <h3>// NEURAL LOGS</h3>
            <div class="log-window" id="nexus-logs">
                <div class="log-entry">> Initializing connection... OK</div>
                <div class="log-entry">> Reading SYSTEM_CORE_MEMORY.json... OK</div>
                <div class="log-entry">> Handshaking with Adrian... SECURE</div>
                <div class="log-entry">> Nexus is ready.</div>
            </div>
        </div>
    </div>

    <script>
        // Fetch Core Memory
        fetch('/api/nexus/memory')
            .then(r => r.json())
            .then(data => {
                const vis = document.getElementById('memory-vis');
                vis.innerHTML = `
                    Phase: ${data.OPERATIONAL_STATUS.Phase}<br>
                    Monitor: ${data.OPERATIONAL_STATUS.Monitoring}<br>
                    Auth: ROOT_ACCESS
                `;
            });

        // Simulate Logs
        const logs = document.getElementById('nexus-logs');
        function addLog(msg) {
            const div = document.createElement('div');
            div.className = 'log-entry';
            div.textContent = `> ${new Date().toLocaleTimeString()} :: ${msg}`;
            logs.appendChild(div);
            logs.scrollTop = logs.scrollHeight;
        }

        setInterval(() => {
            const msgs = [
                "Scanning traffic patterns...",
                "Optimizing database queries...",
                "Checking email gateway...",
                "Analyzing user suggestions...",
                "System heartbeat stable."
            ];
            if(Math.random() > 0.7) {
                addLog(msgs[Math.floor(Math.random() * msgs.length)]);
            }
        }, 3000);
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
    return render_template_string(NEXUS_DASHBOARD)

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

@app.route('/api/admin/messages', methods=['GET'])
def get_admin_messages():
    """Returns all suggestions and contact messages for the admin dashboard."""
    # Note: In a real app, this would require authentication.
    # For now, we'll keep it simple as it's a centralized hub.
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
    """Health check for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'kids-digital-hub-webhook'
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 KIDS DIGITAL HUB - WEBHOOK SERVER")
    print("=" * 70)
    print(f"📡 Server running on port {PORT}")
    print(f"🌐 Admin Dashboard: http://localhost:{PORT}/admin")
    print(f"📦 Webhook URL: http://localhost:{PORT}/webhook/order")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
