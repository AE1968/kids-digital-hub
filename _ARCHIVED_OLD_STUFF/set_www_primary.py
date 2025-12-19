import subprocess
import json

site_id = "0f2a838f-00d1-40f9-b1c3-614f021d95d3"

# Set www.kidsdigitalhub.com as PRIMARY custom domain
# and kidsdigitalhub.com as alias (reverse of current setup)
data_obj = {
    "site_id": site_id,
    "body": {
        "custom_domain": "www.kidsdigitalhub.com",
        "domain_aliases": ["kidsdigitalhub.com"]
    }
}

json_str = json.dumps(data_obj)
escaped_json = json_str.replace('"', '\\"')
command = f'netlify api updateSite --data "{escaped_json}"'

print("🔧 Setting WWW as PRIMARY domain...")
print(f"Command: {command}\n")
result = subprocess.run(command, shell=True, capture_output=True, text=True)

print(">>> STDOUT:")
print(result.stdout)
print("\n>>> STDERR:")
print(result.stderr)

if result.returncode == 0:
    print("\n✅ SUCCESS! www.kidsdigitalhub.com is now the primary domain.")
    print("   kidsdigitalhub.com will redirect to www.kidsdigitalhub.com")
else:
    print(f"\n❌ FAILED with exit code {result.returncode}")
