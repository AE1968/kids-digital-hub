import requests

print("🧪 Test 1: Accesare https://kidsdigitalhub.com (fără www)")
print("=" * 60)

response = requests.get("https://kidsdigitalhub.com", allow_redirects=False)
print(f"Status Code: {response.status_code}")
print(f"Headers:")
for key, value in response.headers.items():
    if key.lower() in ['location', 'server', 'cf-ray']:
        print(f"  {key}: {value}")

if response.status_code in [301, 302, 307, 308]:
    print(f"\n✅ REDIRECT DETECTAT!")
    print(f"   Destinație: {response.headers.get('Location')}")
    
    # Follow redirect
    print("\n🔄 Urmăresc redirect-ul...")
    final_response = requests.get("https://kidsdigitalhub.com", allow_redirects=True)
    print(f"   URL final: {final_response.url}")
    print(f"   Status final: {final_response.status_code}")
else:
    print(f"\n⚠️ NU există redirect (status {response.status_code})")

print("\n" + "=" * 60)
print("🧪 Test 2: Accesare directă https://www.kidsdigitalhub.com")
print("=" * 60)

response2 = requests.get("https://www.kidsdigitalhub.com", allow_redirects=False)
print(f"Status Code: {response2.status_code}")
print(f"URL final: {response2.url if hasattr(response2, 'url') else 'N/A'}")

if response2.status_code == 200:
    print("✅ WWW se încarcă direct fără redirect!")
