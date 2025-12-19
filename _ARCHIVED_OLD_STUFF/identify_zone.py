"""
Identificare automată Zone ID Cloudflare pentru kidsdigitalhub.com
"""

import subprocess
import re

print("🔍 Identificare Zone ID pentru kidsdigitalhub.com...")
print()

# Încearcă să obții Zone ID din DNS records
try:
    result = subprocess.run(
        ["nslookup", "-type=NS", "kidsdigitalhub.com"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    print("📋 DNS Nameservers:")
    print(result.stdout)
    
    if "cloudflare" in result.stdout.lower():
        print("\n✅ Domeniul folosește Cloudflare DNS")
        print("\n📍 Pentru a obține Zone ID și API Token:")
        print("   1. Deschide: https://dash.cloudflare.com")
        print("   2. Login cu contul tău")
        print("   3. Click pe 'kidsdigitalhub.com'")
        print("   4. În dreapta, secțiunea 'API' → Zone ID (copiază)")
        print("   5. Profile → API Tokens → Create Token")
        print("      - Template: 'Edit zone DNS'")
        print("      - Permissions: Zone.Page Rules.Edit")
        print()
        print("📝 Apoi rulează:")
        print("   python cleanup_cloudflare.py")
        print()
    else:
        print("\n⚠️  Domeniul nu pare să folosească Cloudflare")
        
except Exception as e:
    print(f"\n❌ Eroare: {e}")

print("\n" + "="*70)
print("ALTERNATIVĂ: Configurare prin netlify.toml")
print("="*70)
print("""
Am configurat deja redirect-ul în netlify.toml:
  www.kidsdigitalhub.com → kidsdigitalhub.com (301)

Acest redirect va funcționa AUTOMAT după ce ștergi Page Rule-ul
greșit din Cloudflare (cel cu sintaxa 'concat()').

Durează doar 30 de secunde manual:
  1. https://dash.cloudflare.com
  2. kidsdigitalhub.com → Rules → Page Rules
  3. Delete regula cu 'concat()'
  4. GATA!
""")
