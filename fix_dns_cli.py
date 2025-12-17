
import subprocess
import json
import os

site_id = "0f2a838f-00d1-40f9-b1c3-614f021d95d3"
data_obj = {
    "site_id": site_id,
    "body": {
        "custom_domain": "kidsdigitalhub.com",
        "domain_aliases": ["www.kidsdigitalhub.com"]
    }
}

json_str = json.dumps(data_obj)
# Critical: Escape double quotes for Windows Command Line
# In CMD, we wrap in double quotes, and escape inner quotes with backslash
escaped_json = json_str.replace('"', '\\"')

print("🔧 AUTOMATED ARCHITECT FIX: Configuring Domain Alias via Netlify CLI...")

# Command construction
# We use shell=True so we are passing a string command
command = f'netlify api updateSite --data "{escaped_json}"'

try:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    print("\n--- API RESPONSE ---")
    print(result.stdout)
    
    if result.returncode != 0:
        print("\n--- API ERROR LOG ---")
        print(result.stderr)
    else:
        print("\n✅ SUCCESS: 'www.kidsdigitalhub.com' has been formally added to Netlify configuration.")
        
except Exception as e:
    print(f"\n❌ FATAL SCRIPT ERROR: {e}")
