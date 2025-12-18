"""
🚀 CLOUDFLARE PAGE RULES - ȘTERGERE AUTOMATĂ
Versiune simplificată - folosește credențiale salvate
"""

import requests
import json

print("=" * 70)
print("🚀 CLOUDFLARE PAGE RULES - CLEANUP AUTOMAT")
print("=" * 70)

# Credențiale salvate
ZONE_ID = "649af348789563231acc661c2ef415ac5a7ce"
EMAIL = "adrianencl1@gmail.com"

print("\n📋 Folosesc credențiale salvate:")
print(f"   Email: {EMAIL}")
print(f"   Zone ID: {ZONE_ID}")

# Solicită doar API Token
print("\n🔑 Introdu Cloudflare API Token:")
print("   (Găsești la: https://dash.cloudflare.com/profile/api-tokens)")
print("   Sau apasă ENTER pentru a deschide browser-ul și a-l obține automat")
print()

API_TOKEN = input("API Token (sau ENTER pentru automat): ").strip()

if not API_TOKEN:
    print("\n🌐 Deschid browser-ul pentru a obține API Token automat...")
    print("   Te voi ghida pas cu pas!")
    import webbrowser
    webbrowser.open("https://dash.cloudflare.com/profile/api-tokens")
    
    print("\n📋 Pași:")
    print("   1. Click 'Create Token'")
    print("   2. Alege 'Edit zone DNS' template")
    print("   3. Zone Resources: Include → Specific zone → kidsdigitalhub.com")
    print("   4. Click 'Continue to summary' → 'Create Token'")
    print("   5. COPIAZĂ token-ul afișat")
    print()
    
    API_TOKEN = input("Paste API Token aici: ").strip()

if not API_TOKEN:
    print("\n❌ EROARE: API Token este obligatoriu!")
    exit(1)

# Configurare API
BASE_URL = f"https://api.cloudflare.com/v4/zones/{ZONE_ID}/pagerules"
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

print("\n" + "=" * 70)
print("PASUL 1: Verificare Page Rules Existente")
print("=" * 70)

try:
    response = requests.get(BASE_URL, headers=headers)
    
    if response.status_code == 403:
        print("\n❌ EROARE: API Token nu are permisiuni suficiente!")
        print("   Creează un nou token cu:")
        print("   - Zone → Zone Settings → Edit")
        print("   - Zone → Page Rules → Edit")
        exit(1)
    
    if response.status_code == 401:
        print("\n❌ EROARE: API Token invalid sau expirat!")
        exit(1)
    
    response.raise_for_status()
    data = response.json()
    
    if not data.get("success"):
        print(f"\n❌ EROARE API: {data.get('errors', 'Unknown error')}")
        exit(1)
    
    rules = data["result"]
    
    print(f"\n✅ Găsite {len(rules)} Page Rules:\n")
    
    if len(rules) == 0:
        print("✅ Nu există Page Rules de șters!")
        print("   Redirect-ul va funcționa prin netlify.toml")
        print("\n🎯 GATA! Site-ul ar trebui să funcționeze acum.")
        print("   Testează: https://www.kidsdigitalhub.com")
        exit(0)
    
    for idx, rule in enumerate(rules, 1):
        print(f"{idx}. ID: {rule['id']}")
        print(f"   URL Pattern: {rule['targets'][0]['constraint']['value']}")
        print(f"   Status: {rule['status']}")
        
        if rule.get('actions'):
            for action in rule['actions']:
                if action['id'] == 'forwarding_url':
                    dest = action['value'].get('url', 'N/A')
                    print(f"   Redirect: {dest}")
        print("-" * 70)
    
except requests.exceptions.RequestException as e:
    print(f"\n❌ EROARE la conectare: {e}")
    exit(1)

print("\n" + "=" * 70)
print("PASUL 2: Ștergere Page Rules Problematice")
print("=" * 70)

deleted_count = 0
errors = []

for rule in rules:
    url_pattern = rule['targets'][0]['constraint']['value']
    rule_id = rule['id']
    
    # Șterge orice Page Rule care conține kidsdigitalhub.com
    if 'kidsdigitalhub.com' in url_pattern.lower():
        print(f"\n🗑️  Șterg Page Rule: {url_pattern}")
        print(f"   ID: {rule_id}")
        
        try:
            delete_response = requests.delete(f"{BASE_URL}/{rule_id}", headers=headers)
            delete_response.raise_for_status()
            
            delete_data = delete_response.json()
            if delete_data.get("success"):
                print(f"   ✅ Șters cu succes!")
                deleted_count += 1
            else:
                error_msg = delete_data.get('errors', 'Unknown error')
                print(f"   ❌ Eroare: {error_msg}")
                errors.append(f"{url_pattern}: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Eroare la ștergere: {e}")
            errors.append(f"{url_pattern}: {e}")

print("\n" + "=" * 70)
print(f"✅ CLEANUP COMPLET!")
print("=" * 70)
print(f"\n📊 Statistici:")
print(f"   • Page Rules șterse: {deleted_count}")
print(f"   • Erori: {len(errors)}")

if errors:
    print(f"\n⚠️  Erori întâlnite:")
    for error in errors:
        print(f"   - {error}")

print("\n📋 CONFIGURARE FINALĂ:")
print("   • Netlify gestionează redirect-ul prin netlify.toml")
print("   • kidsdigitalhub.com → www.kidsdigitalhub.com (301)")
print("   • Cloudflare face doar DNS proxying")

print("\n⏱️  Așteaptă 2-3 minute pentru propagare DNS")
print("\n🎯 TESTEAZĂ:")
print("   https://www.kidsdigitalhub.com")
print("   https://kidsdigitalhub.com (ar trebui să redirecționeze)")

print("\n✅ GATA! Site-ul ar trebui să funcționeze perfect!")
print()
