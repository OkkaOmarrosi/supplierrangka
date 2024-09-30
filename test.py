import requests

response = requests.get('http:///api/products')
print(response.json())
