import requests

url = 'http://localhost:9696/predict'
data = {'url':'https://healthy.thewom.it/wp-content/uploads/2009/09/Polmonite-ai-raggi-X-300x233.jpg'}
result = requests.post(url, json=data).json()
print(result)
