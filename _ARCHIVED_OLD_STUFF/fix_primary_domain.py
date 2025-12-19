import subprocess
import json

site_id = "0f2a838f-00d1-40f9-b1c3-614f021d95d3"
data_obj = {
    "site_id": site_id,
    "body": {
        "custom_domain": "kidsdigitalhub.com",
        "domain_aliases": ["www.kidsdigitalhub.com"]
    }
}

json_str = json.dumps(data_obj)
# In PowerShell/CMD, we need to escape quotes carefully or use a pipe
# Let's try writing it to a file and using that
with open('site_config.json', 'w') as f:
    f.write(json_str)

print("🔧 Setting kidsdigitalhub.com as PRIMARY domain...")
# Netlify CLI doesn't easily take a file for updateSite via --data
# But we can read it in python and pass it as a single string
escaped_json = json_str.replace('"', '\\"')
command = f'netlify api updateSite --data "{escaped_json}"'

result = subprocess.run(command, shell=True, capture_output=True, text=True)

print(">>> STDOUT:")
print(result.stdout)
print("\n>>> STDERR:")
print(result.stderr)

if result.returncode == 0:
    print("\n✅ SUCCESS! kidsdigitalhub.com is now the primary domain.")
else:
    print(f"\n❌ FAILED with exit code {result.returncode}")
