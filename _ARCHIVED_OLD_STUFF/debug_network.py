
import socket
import requests

def check_domain(domain):
    print(f"\nChecking {domain}...")
    try:
        ip = socket.gethostbyname(domain)
        print(f"  ✅ DNS Resolved: {ip}")
    except Exception as e:
        print(f"  ❌ DNS Failed: {e}")
        return

    try:
        response = requests.get(f"http://{domain}", timeout=5)
        print(f"  ✅ HTTP Status: {response.status_code}")
        if response.status_code == 404:
            print("     ⚠️  Server reachable, but return 404 (Likely Configuration Missing)")
        elif response.status_code == 200:
            print("     🎉 Success!")
    except Exception as e:
        print(f"  ❌ HTTP Failed: {e}")

check_domain("kidsdigitalhub.com")
check_domain("www.kidsdigitalhub.com")
print("\nChecking Netlify Direct URL...")
check_domain("friendly-sawine-0d5dd4.netlify.app")
