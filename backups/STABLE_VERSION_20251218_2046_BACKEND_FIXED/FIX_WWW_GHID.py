"""
🚀 SOLUȚIE RAPIDĂ: Șterge Page Rules din Cloudflare
"""

print("=" * 70)
print("🔧 FIX WWW REDIRECT - GHID PAS CU PAS")
print("=" * 70)

print("""
PROBLEMA IDENTIFICATĂ:
----------------------
Cloudflare are un Page Rule greșit care folosește sintaxa 'concat()'.
Aceasta este pentru Transform Rules, NU pentru Page Rules.

SOLUȚIA:
--------
Trebuie să ștergi Page Rule-ul din Cloudflare Dashboard.

PAȘI:
-----
1. Deschide: https://dash.cloudflare.com
2. Selectează domeniul: kidsdigitalhub.com
3. Click pe: Rules → Page Rules
4. Găsește regula care conține 'concat' sau 'kidsdigitalhub.com'
5. Click pe butonul de Edit (creion)
6. Scroll jos și click pe Delete (roșu)
7. Confirmă ștergerea

SAU - Dacă vrei să rulez scriptul automat:
------------------------------------------
Ai nevoie de:
  • Zone ID (găsești în Overview → API)
  • API Token (creezi la: Profile → API Tokens → Create Token)
    - Template: "Edit zone DNS"
    - Permissions: Zone.Page Rules.Edit

Apoi rulează:
  python fix_cloudflare_redirect.py

VERIFICARE DUPĂ ȘTERGERE:
-------------------------
curl -I https://www.kidsdigitalhub.com

Ar trebui să vezi:
  HTTP/2 301
  Location: https://kidsdigitalhub.com/
  Server: Netlify

IMPORTANT:
----------
După ștergere, Netlify va prelua automat redirect-ul prin netlify.toml
(care este deja configurat corect).

Așteaptă 2-3 minute pentru propagare DNS.
""")

print("\n" + "=" * 70)
print("Vrei să continui cu scriptul automat? (y/n)")
choice = input("> ").strip().lower()

if choice == 'y':
    print("\n📋 Introdu credențialele Cloudflare:")
    zone_id = input("Zone ID: ").strip()
    api_token = input("API Token: ").strip()
    
    if zone_id and api_token:
        print("\n✅ Credențiale primite! Rulez scriptul de cleanup...")
        import subprocess
        subprocess.run([
            "python", "fix_cloudflare_redirect.py"
        ], env={
            "CF_ZONE_ID": zone_id,
            "CF_API_TOKEN": api_token
        })
    else:
        print("\n❌ Credențiale incomplete!")
else:
    print("\n👉 Șterge manual Page Rule-ul din Cloudflare Dashboard")
    print("   Link direct: https://dash.cloudflare.com")
