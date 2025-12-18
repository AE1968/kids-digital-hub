"""
🔧 CLOUDFLARE PAGE RULES CLEANUP - VERSIUNE AUTOMATĂ
Șterge toate Page Rules problematice pentru kidsdigitalhub.com
"""

import requests
import json

print("=" * 70)
print("🚀 CLOUDFLARE PAGE RULES - CLEANUP AUTOMAT")
print("=" * 70)

# Credențiale Cloudflare
print("\n📋 Introdu credențialele Cloudflare:")
print("   Găsești la: https://dash.cloudflare.com/profile/api-tokens")
print()

ZONE_ID = input("Zone ID pentru kidsdigitalhub.com: ").strip()
API_TOKEN = input("API Token (cu permisiuni Zone Settings): ").strip()

if not ZONE_ID or not API_TOKEN:
    print("\n❌ EROARE: Credențiale incomplete!")
    print("\n📍 Unde găsești credențialele:")
    print("   1. Zone ID: Cloudflare Dashboard → kidsdigitalhub.com → Overview → API (coloana dreapta)")
    print("   2. API Token: Cloudflare Dashboard → Profile → API Tokens → Create Token")
    print("      - Template: 'Edit zone DNS'")
    print("      - Permissions: Zone → Zone Settings → Edit")
    exit(1)

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
    
    response.raise_for_status()
    data = response.json()
    
    if not data.get("success"):
        print(f"\n❌ EROARE API: {data.get('errors', 'Unknown error')}")
        exit(1)
    
    rules = data["result"]
    
    print(f"\n✅ Găsite {len(rules)} Page Rules:\n")
    
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

if len(rules) == 0:
    print("\n✅ Nu există Page Rules de șters!")
    print("   Redirect-ul va funcționa prin netlify.toml")
    exit(0)

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
print("   • Netlify va gestiona redirect-ul prin netlify.toml")
print("   • www.kidsdigitalhub.com → kidsdigitalhub.com (301)")
print("   • Cloudflare face doar DNS proxying")

print("\n⏱️  Așteaptă 2-3 minute pentru propagare DNS")
print("🧪 Testează cu: curl -I https://www.kidsdigitalhub.com")
print("\n✅ Ar trebui să vezi:")
print("   HTTP/2 301")
print("   Location: https://kidsdigitalhub.com/")
print("   Server: Netlify")
print()
