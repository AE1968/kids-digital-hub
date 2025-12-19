
import subprocess
import json

site_id = "0f2a838f-00d1-40f9-b1c3-614f021d95d3"
# Try ONLY updating domain_aliases, avoiding potential conflict with existing custom_domain field
data_obj = {
    "site_id": site_id,
    "body": {
        "domain_aliases": ["www.kidsdigitalhub.com"]
    }
}

json_str = json.dumps(data_obj)
escaped_json = json_str.replace('"', '\\"')
command = f'netlify api updateSite --data "{escaped_json}"'

print("🔧 RETRY: Adding 'www' alias only...")
result = subprocess.run(command, shell=True, capture_output=True, text=True)

print("\n>>> STDOUT:")
print(result.stdout)
print("\n>>> STDERR:")
print(result.stderr)
