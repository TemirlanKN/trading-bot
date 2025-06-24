import requests

webhook_url = "https://ktim9908.app.n8n.cloud/webhook-test/01ccec63-5b71-4977-9159-9aefcccd9c7f"
data = {"message": "Hello from Python!"}

response = requests.post(webhook_url, json=data)
print("Status code:", response.status_code)
print("Response:", response.text)
