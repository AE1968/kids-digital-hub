import requests
import datetime

def check_url(url, name):
    try:
        start = datetime.datetime.now()
        response = requests.get(url, timeout=10)
        end = datetime.datetime.now()
        duration = (end - start).total_seconds()
        return {
            "name": name,
            "url": url,
            "status": response.status_code,
            "latency": f"{duration:.2f}s",
            "alive": response.status_code == 200
        }
    except Exception as e:
        return {
            "name": name,
            "url": url,
            "status": "ERROR",
            "latency": "N/A",
            "alive": False,
            "error": str(e)
        }

def generate_report():
    print(f"📊 LIVE SYSTEM DIAGNOSTIC REPORT")
    print(f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    services = [
        ("Frontend (WWW)", "https://www.kidsdigitalhub.com"),
        ("Frontend (Root)", "https://kidsdigitalhub.com"),
        ("Backend Admin", "https://web-production-b215.up.railway.app/admin"),
        ("Nexus Brain API", "https://web-production-b215.up.railway.app/webhook/order") # Checking webhook endpoint
    ]
    
    all_systems_go = True
    
    for name, url in services:
        result = check_url(url, name)
        status_icon = "✅" if result["alive"] or result["status"] == 405 else "❌" # 405 is fine for POST-only webhook
        if result["status"] == 405: status_icon = "✅ (Method Not Allowed - Good)"
        
        print(f"{status_icon} {result['name']}")
        print(f"   URL: {result['url']}")
        print(f"   Status: {result['status']}")
        print(f"   Latency: {result['latency']}")
        print("-" * 50)
        
        if not result["alive"] and result["status"] != 405:
            all_systems_go = False

    if all_systems_go:
        print("\n🚀 CONCLUSION: ALL CRITICAL SYSTEMS OPERATIONAL")
    else:
        print("\n⚠️ CONCLUSION: SYSTEM ISSUES DETECTED")

if __name__ == "__main__":
    generate_report()
