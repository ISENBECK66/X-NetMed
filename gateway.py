import grpc # usiamo questo protocollo per comunicare tra le due entità : gateway <-> classifier
#import tensorflow as tf ---> libraria troppo grande da includere in un environment

import os # let the two dockers communicate

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

from keras_image_helper import create_preprocessor

from flask import Flask
from flask import request
from flask import jsonify


from proto import np_to_protobuf # ---> importiamo solo questa al posto di tf

host = os.getenv('TF_SERVING_HOST','localhost:8500') # address configurable, otherwise localhost:8500 as default
#host = 'localhost:8500' # we want to remove this, where the address is hardcoded

channel = grpc.insecure_channel(host, options=(('grpc.enable_http_proxy', 0),)) # is local, otherwise we need authentication etc.
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)  

preprocessor = create_preprocessor('resnet50',target_size=(224,224))

#def np_to_protobuf(data):
 #   return tf.make_tensor_proto(data,shape=data.shape) 
    
def prepare_request(X):
	pb_request = predict_pb2.PredictRequest()

	pb_request.model_spec.name = 'chest_xray-model' # specified in the docker created for TF-serving
	pb_request.model_spec.signature_name = 'serving_default' # name from the converted model information script
	pb_request.inputs['input_12'].CopyFrom(np_to_protobuf(X)) # CopyFrom it means '=' : we are passing X as input

	return pb_request
	
classes = [
 'NORMAL',
 'PNEUMONIA'
]

def prepare_response(pb_response):
	pred = pb_response.outputs['dense_7'].float_val # gli passiamo il valore output letto nel file!
	if pred[0]>pred[1]:
		return 0	
	return 1
	

def predict(url):
	X = preprocessor.from_url(url)
	pb_request = prepare_request(X)
	pb_response = stub.Predict(pb_request, timeout=20.0)
	response = prepare_response(pb_response)
	return response
	
app = Flask('gateway')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
	data = request.get_json()
	url = data['url']
	result = predict(url)
	return jsonify(result)	
	
if __name__ == '__main__':
#	url ='https://healthy.thewom.it/wp-content/uploads/2009/09/Polmonite-ai-raggi-X-300x233.jpg'
#	response = predict(url)
#	print(response)
	app.run(debug=True, host='0.0.0.0', port=9696)
