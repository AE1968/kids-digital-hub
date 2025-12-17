"""
Script pentru trimiterea raportului zilnic automat pe email.
Rulează pe server (GitHub Actions) după generarea produselor.
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests

# Configurare
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER') # Email-ul tau (adrianenc11@gmail.com)
SMTP_PASS = os.getenv('SMTP_PASS') # App Password generat din Google Account
TO_EMAIL = os.getenv('TO_EMAIL', 'adrianenc11@gmail.com')

SITE_URL = "https://friendly-sawine-0d5dd4.netlify.app" # Sau kidsdigitalhub.com

def load_stats():
    """Încarcă statisticile salvate"""
    stats = {}
    try:
        with open("site_statistics.json", "r", encoding="utf-8") as f:
            stats = json.load(f)
    except Exception as e:
        print(f"⚠️ Nu s-au putut citi statisticile: {e}")
    return stats

def load_logs():
    """Încarcă log-urile de generare"""
    logs = []
    try:
        with open("generation_log.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
    except Exception as e:
        print(f"⚠️ Nu s-au putut citi log-urile: {e}")
    return logs

def check_site_status():
    """Verifică dacă site-ul este online"""
    try:
        response = requests.get(SITE_URL, timeout=10)
        return {
            "status": "ONLINE" if response.status_code == 200 else f"OFFLINE ({response.status_code})",
            "code": response.status_code,
            "latency": f"{response.elapsed.total_seconds():.2f}s"
        }
    except Exception as e:
        return {"status": "ERROR", "code": 0, "latency": "0s", "error": str(e)}

def create_email_body(stats, last_log, site_status):
    """Creează corpul emailului în format HTML"""
    
    products_generated = last_log.get('products_generated', 0) if last_log else 0
    total_products = stats.get('total_products', 0)
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden;">
            <div style="background: #4CAF50; color: white; padding: 20px; text-align: center;">
                <h2 style="margin: 0;">📊 Raport Zilnic Kids Digital Hub</h2>
                <p style="margin: 5px 0 0;">{datetime.now().strftime('%d %B %Y')}</p>
            </div>
            
            <div style="padding: 20px;">
                <h3 style="color: #2E7D32; border-bottom: 2px solid #eee; padding-bottom: 10px;">🚀 Activitate Server & Generare AI</h3>
                <p><strong>Status Generare:</strong> <span style="color: green;">✅ SUCCES</span></p>
                <p>Au fost generate și publicate <strong>{products_generated} produse noi</strong> astăzi.</p>
                
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr style="background: #f9f9f9;">
                        <td style="padding: 10px; border: 1px solid #eee;">📦 Total Produse în Catalog</td>
                        <td style="padding: 10px; border: 1px solid #eee; font-weight: bold;">{total_products}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #eee;">💰 Produse Premium</td>
                        <td style="padding: 10px; border: 1px solid #eee;">{stats.get('paid_products', 0)}</td>
                    </tr>
                    <tr style="background: #f9f9f9;">
                        <td style="padding: 10px; border: 1px solid #eee;">🎁 Produse Gratuite</td>
                        <td style="padding: 10px; border: 1px solid #eee;">{stats.get('free_products', 0)}</td>
                    </tr>
                </table>

                <h3 style="color: #1976D2; border-bottom: 2px solid #eee; padding-bottom: 10px;">🌐 Status Website</h3>
                <p><strong>URL:</strong> <a href="{SITE_URL}">{SITE_URL}</a></p>
                <p><strong>Status:</strong> <span style="background: #E8F5E9; color: #2E7D32; padding: 3px 8px; border-radius: 4px; font-weight: bold;">{site_status['status']}</span></p>
                <p><strong>Timp răspuns:</strong> {site_status['latency']}</p>

                <h3 style="color: #E65100; border-bottom: 2px solid #eee; padding-bottom: 10px;">📊 Statistici Vizitatori</h3>
                <ul>
                    <li>👀 Vizualizări Totale: <strong>{stats.get('total_views', 0):,}</strong></li>
                    <li>🛒 Vânzări Totale: <strong>{stats.get('total_sales', 0):,}</strong></li>
                </ul>

                <div style="background: #FFF3E0; padding: 15px; border-radius: 5px; margin-top: 20px; font-size: 0.9em;">
                    <p style="margin: 0;"><em>Acest raport a fost generat automat de serverul Kids Digital Hub.</em></p>
                </div>
            </div>
            
            <div style="background: #f4f4f4; padding: 10px; text-align: center; font-size: 0.8em; color: #666;">
                &copy; {datetime.now().year} Kids Digital Hub Automation System
            </div>
        </div>
    </body>
    </html>
    """
    return html

def send_email():
    print("📧 Pregătire raport email...")
    
    if not SMTP_USER or not SMTP_PASS:
        print("⚠️  SMTP_USER sau SMTP_PASS lipsesc. Nu se poate trimite emailul.")
        print("ℹ️  Setează secretele în GitHub: SMTP_USER (email) și SMTP_PASS (app password).")
        return

    stats = load_stats()
    logs = load_logs()
    last_log = logs[-1] if logs else {}
    site_status = check_site_status()
    
    html_content = create_email_body(stats, last_log, site_status)
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"📊 Raport Zilnic: {stats.get('total_products', 0)} Produse - {datetime.now().strftime('%d/%m/%Y')}"
    msg['From'] = f"Kids Hub Admin <{SMTP_USER}>"
    msg['To'] = TO_EMAIL
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        print(f"📡 Conectare la {SMTP_HOST}...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            print("✅ Email trimis cu succes către adrianenc11@gmail.com!")
    except Exception as e:
        print(f"❌ Eroare la trimiterea emailului: {e}")

if __name__ == "__main__":
    send_email()
