"""
Flask Webhook Server for Automatic Order Processing
Runs on Railway.app or any cloud platform
"""

from flask import Flask, request, jsonify, render_template_string
import os
import json
import hmac
import hashlib
from datetime import datetime
from webhook_order_handler import process_new_order

app = Flask(__name__)

# Configuration
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-secret-key-change-this')
PORT = int(os.getenv('PORT', 8080))

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
            <h2>⚙️ System Configuration</h2>
            <p><strong>🔑 Printful API:</strong> <span class="status active">Configured</span></p>
            <p><strong>🤖 Google AI API:</strong> <span class="status active">Configured</span></p>
            <p><strong>🌐 Webhook URL:</strong> <code>{{ webhook_url }}</code></p>
            <p><strong>📅 Last Update:</strong> {{ last_update }}</p>
            <br>
            <button class="btn" onclick="testWebhook()">🧪 Test Webhook</button>
            <button class="btn" onclick="generateProducts()">🎨 Generate New Products</button>
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
    
    return render_template_string(
        ADMIN_DASHBOARD,
        total_orders=len(orders),
        total_products=stats.get('total_products', 0),
        total_revenue=stats.get('total_sales', 0) * 7.5,  # Estimated profit
        recent_orders=reversed(recent_orders),
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
