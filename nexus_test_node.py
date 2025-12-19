import requests
try:
    r = requests.get('https://www.kidsdigitalhub.com', timeout=5)
    print(f'Status: {r.status_code}, Redirects: {len(r.history)}')
except Exception as e:
    print(f'Error: {str(e)}')
