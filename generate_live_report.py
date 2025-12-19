import requests
import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_url(url, name):
    try:
        start = datetime.datetime.now()
        # verify=False helps if local CA certs are missing
        response = requests.get(url, timeout=10, verify=False)
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
        ("Backend Core", "https://web-production-b215.up.railway.app/"),
        ("Nexus Brain API", "https://web-production-b215.up.railway.app/webhook/order") 
    ]
    
    all_systems_go = True
    
    for name, url in services:
        result = check_url(url, name)
        status_icon = "✅" if result["alive"] or result["status"] == 405 else "❌"
        if result["status"] == 405: status_icon = "✅ (Method Not Allowed - Good)"
        
        print(f"{status_icon} {result['name']}")
        print(f"   URL: {result['url']}")
        print(f"   Status: {result['status']}")
        if result.get('error'):
            print(f"   ⚠️ Error Details: {result['error']}")
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
