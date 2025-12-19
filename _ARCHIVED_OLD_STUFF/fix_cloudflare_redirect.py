"""
Script automat pentru ștergerea Page Rules greșite din Cloudflare
și verificarea configurației DNS
"""

import requests
import json
import sys

print("=" * 70)
print("🔧 CLOUDFLARE PAGE RULES - CLEANUP AUTOMAT")
print("=" * 70)

# Solicită credențiale
print("\n📋 Introdu credențialele Cloudflare:")
print("   (Le găsești la: https://dash.cloudflare.com/profile/api-tokens)")
print()

ZONE_ID = input("Zone ID pentru kidsdigitalhub.com: ").strip()
API_TOKEN = input("Cloudflare API Token (cu permisiuni Zone.Page Rules): ").strip()

if not ZONE_ID or not API_TOKEN:
    print("\n❌ EROARE: Zone ID și API Token sunt obligatorii!")
    sys.exit(1)

BASE_URL = f"https://api.cloudflare.com/v4/zones/{ZONE_ID}/pagerules"
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

print("\n" + "=" * 70)
print("PASUL 1: Listare Page Rules Existente")
print("=" * 70)

try:
    response = requests.get(BASE_URL, headers=headers)
    response.raise_for_status()
    rules = response.json()["result"]
    
    print(f"\n✅ Găsite {len(rules)} Page Rules:\n")
    
    for idx, rule in enumerate(rules, 1):
        print(f"{idx}. ID: {rule['id']}")
        print(f"   URL: {rule['targets'][0]['constraint']['value']}")
        print(f"   Status: {rule['status']}")
        
        if rule.get('actions'):
            for action in rule['actions']:
                if action['id'] == 'forwarding_url':
                    print(f"   Redirect: {action['value']['url']}")
        print("-" * 70)
    
except requests.exceptions.RequestException as e:
    print(f"\n❌ EROARE la listare: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("PASUL 2: Ștergere Page Rules Problematice")
print("=" * 70)

deleted_count = 0

for rule in rules:
    url_pattern = rule['targets'][0]['constraint']['value']
    rule_id = rule['id']
    
    # Șterge orice Page Rule care conține kidsdigitalhub.com
    if 'kidsdigitalhub.com' in url_pattern:
        print(f"\n🗑️  Șterg Page Rule: {url_pattern}")
        print(f"   ID: {rule_id}")
        
        try:
            delete_response = requests.delete(f"{BASE_URL}/{rule_id}", headers=headers)
            delete_response.raise_for_status()
            print(f"   ✅ Șters cu succes!")
            deleted_count += 1
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Eroare la ștergere: {e}")

print("\n" + "=" * 70)
print(f"✅ CLEANUP COMPLET! {deleted_count} Page Rules șterse")
print("=" * 70)

print("\n📋 CONFIGURARE FINALĂ:")
print("   • Netlify va gestiona redirect-ul prin netlify.toml")
print("   • www.kidsdigitalhub.com → kidsdigitalhub.com (301)")
print("   • Cloudflare va face doar DNS proxying")

print("\n⏱️  Așteaptă 2-3 minute pentru propagare")
print("🧪 Testează cu: curl -I https://www.kidsdigitalhub.com")
print()
