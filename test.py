import requests

url = 'http://localhost:9696/predict'
print()
x= input("Please enter the url of the chest xray :	")
print()
data = {'url':x} # https://healthy.thewom.it/wp-content/uploads/2009/09/Polmonite-ai-raggi-X-300x233.jpg'}

#print(data)

result = requests.post(url, json=data).json()

#print(result)

if result==1:
	print("		>>>>>>>>>>>>>>>>>>>>>>>>>  PNEUMONIA SEVERE WARNING !!!  <<<<<<<<<<<<<<<<<<<<<<<<<")
else:	
	print("		>>>>>>>>>>>>>>>>>>>>>>>>>  Your X-RAY are OK !!!  <<<<<<<<<<<<<<<<<<<<<<<<<")
	
print()
print()

