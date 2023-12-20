import requests

url = 'http://localhost:9696/predict'
data = {'url':'https://github.com/ISENBECK66/ML2023/blob/main/person3_virus_15.jpeg?raw=true'}
result = requests.post(url, json=data).json()

#print(result)

if result==1:
	print("		>>>>>>>>>>>>>>>>>>>>>>>>>  PNEUMONIA SEVERE WARNING !!!  <<<<<<<<<<<<<<<<<<<<<<<<<")
else:	
	print("		>>>>>>>>>>>>>>>>>>>>>>>>>  X-RAY negative to pneumonia, you are OK !  <<<<<<<<<<<<<<<<<<<<<<<<<")
	
print()
print()
