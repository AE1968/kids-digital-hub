"""
Script pentru configurarea redirect-ului INVERS în Cloudflare
De la: kidsdigitalhub.com → www.kidsdigitalhub.com
"""

import requests
import json

# Configurare
ZONE_ID = input("Introdu Zone ID pentru kidsdigitalhub.com: ").strip()
API_TOKEN = input("Introdu Cloudflare API Token: ").strip()

BASE_URL = f"https://api.cloudflare.com/v4/zones/{ZONE_ID}/pagerules"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

print("\n" + "="*60)
print("PASUL 1: Verificare Page Rules existente")
print("="*60)

# Listează toate Page Rules
response = requests.get(BASE_URL, headers=headers)
if response.status_code == 200:
    rules = response.json()["result"]
    print(f"✅ Găsite {len(rules)} Page Rules existente:\n")
    
    for rule in rules:
        print(f"ID: {rule['id']}")
        print(f"URL: {rule['targets'][0]['constraint']['value']}")
        print(f"Status: {rule['status']}")
        if rule.get('actions'):
            for action in rule['actions']:
                if action['id'] == 'forwarding_url':
                    print(f"Redirect: {action['value']['url']}")
        print("-" * 40)
    
    # Șterge Page Rules vechi care conțin redirect www
    print("\n" + "="*60)
    print("PASUL 2: Ștergere Page Rules vechi (www redirect)")
    print("="*60)
    
    for rule in rules:
        url_pattern = rule['targets'][0]['constraint']['value']
        if 'www.kidsdigitalhub.com' in url_pattern or 'kidsdigitalhub.com' in url_pattern:
            print(f"\n🗑️  Șterg Page Rule: {url_pattern}")
            delete_response = requests.delete(f"{BASE_URL}/{rule['id']}", headers=headers)
            if delete_response.status_code == 200:
                print(f"✅ Șters cu succes!")
            else:
                print(f"❌ Eroare la ștergere: {delete_response.text}")
else:
    print(f"❌ Eroare la listare: {response.text}")
    exit(1)

print("\n" + "="*60)
print("PASUL 3: Creare Page Rule NOU (non-www → www)")
print("="*60)

# Creează Page Rule NOU pentru redirect INVERS
new_rule = {
    "targets": [
        {
            "target": "url",
            "constraint": {
                "operator": "matches",
                "value": "kidsdigitalhub.com/*"
            }
        }
    ],
    "actions": [
        {
            "id": "forwarding_url",
            "value": {
                "url": "https://www.kidsdigitalhub.com/$1",
                "status_code": 301
            }
        }
    ],
    "priority": 1,
    "status": "active"
}

print("\n📝 Configurare nouă:")
print(f"   Pattern: kidsdigitalhub.com/*")
print(f"   Redirect: https://www.kidsdigitalhub.com/$1")
print(f"   Status Code: 301 (Permanent)")

response = requests.post(BASE_URL, headers=headers, json=new_rule)

if response.status_code == 200:
    print("\n✅ SUCCESS! Page Rule creat cu succes!")
    result = response.json()["result"]
    print(f"\n📋 Detalii:")
    print(f"   ID: {result['id']}")
    print(f"   Status: {result['status']}")
    print(f"   Priority: {result['priority']}")
else:
    print(f"\n❌ EROARE la creare: {response.text}")
    exit(1)

print("\n" + "="*60)
print("PASUL 4: Verificare finală")
print("="*60)

response = requests.get(BASE_URL, headers=headers)
if response.status_code == 200:
    rules = response.json()["result"]
    print(f"\n✅ Total Page Rules active: {len(rules)}")
    for rule in rules:
        print(f"\n   URL: {rule['targets'][0]['constraint']['value']}")
        print(f"   Status: {rule['status']}")

print("\n" + "="*60)
print("✅ CONFIGURARE COMPLETĂ!")
print("="*60)
print("\n📌 Comportament final:")
print("   • kidsdigitalhub.com → REDIRECT la www.kidsdigitalhub.com")
print("   • www.kidsdigitalhub.com → RĂMÂNE în bara de adrese")
print("\n⏱️  Așteaptă 2-3 minute pentru propagare DNS")
print("🧪 Testează cu: curl -I https://kidsdigitalhub.com")
print("\n")
