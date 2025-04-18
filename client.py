import requests

API_URL = "http://34.150.252.67:5000/api/secure-data"
TOKEN = "supersecrettoken123"

headers = {
"Authorization": f"Bearer {TOKEN}"
}

response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
 print("Success:", response.json())
else:
 print("Failed:", response.status_code, response.text)