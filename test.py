import requests

response = requests.get('http://http://127.0.0.1:5000/api/products')
print(response.json())
