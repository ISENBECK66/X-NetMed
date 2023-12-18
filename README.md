# X-NetMed, or: 
## *a Neural Network approach to pneumonia identification in X-rays images*
<img src="https://github.com/ISENBECK66/X-NetMed/blob/main/NORMAL2-IM-0132-0001.jpeg" width="300" height="300"> <img src="https://github.com/ISENBECK66/X-NetMed/blob/main/NORMAL2-IM-0132-0001.jpeg" width="300" height="300"> <img src="https://github.com/ISENBECK66/X-NetMed/blob/main/NORMAL2-IM-0132-0001.jpeg" width="300" height="300">



---

### The importance of a praecox pneumonia infection's diagnosis:

####
Pneumonia is an inflammation in your lungs caused by a bacterial, viral or fungal infection. It makes it difficult to breathe and can cause a fever and cough with yellow, green or bloody mucus. The flu, COVID-19 and pneumococcal disease are common causes of pneumonia. Treatment depends on the cause and severity of pneumonia.
Not surprisingly many consider that chest radiology, which is a relatively inexpensive test, plays a fundamental and important role in the diagnosis of pneumonia, together with clinical assessment and sometimes appropriate microbiological testing. Its primary purpose is to diagnose or exclude pneumonia.

####
---
### Neural Network and Deep Learning to build a binary classifier to elaborate x-ray images:
####
The target of this project is to create a service that automatically verify the presence of a pneumonia infection, using Deep Learning tools on the x-ray images of patient's chest.
We used a Neural Network and a pretrained model that it is been adapted for our scopes.
The choosen pre-trained model it has been *ResNet50* from the *keras* package.
The initial weights for the preprocess of the images come from *imagenet*.
####
--- 
### Dataset:
####
The *dataset* that is been used for train our model come from *Keggle* and contains ~ 6000 x-ray images, splitted in *NORMAL* and *PNEUMONIA* classes.
Here you can find all the information that you need about the dataset :
[https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia]
####
---
### Software architecture :
We decided to develop two services dedicated to two specific functions:
#### TF-Serving (*Model*): 
This function get in input a pre-eleborate image, and it is designed to apply inference on it, using the model that we trained for this pourpouse. 
This function needs a lot of GPU resources to evaluate the images and this is the reason behind our choice to have our application splitted in two different services. 
The *model* is applied on the data that are coming from the *gateway-service*, *TF-Serving* send back to it the results of the elaboration.
#### *Gateway-service*:
This function read the input image from an URL provided from the user through the user interface, and provide the specific pre-elaboration required from the *model*.
After this elaboration the *gateway-service* send the data trought the network to the *TF-Serving* service, and wait to receive back the evaluation.
Once received back the evaluation, the data are organized and adjusted at this level before the answer is sent back to the user through the terminal.

---

### Repository content:
#### - notebook.ipynb file
This repository contains *notebook.ipynb file* : In this file we load the *ResNet50* model and the *dataset* downloaded from kaggle.
We worked on the *model* building on its top our specific *dense layer / inner layer* trained on the images loaded from our *dataset*.     
In the same file we tried different setup to obtain the best performance, tuning model parameters, as : *leraning_rate*, *drop_rate* and *augmentation*.
#### - ResNet50_v2_12_0.950.h5 file
We used the *keras.callbacks.ModelCheckpoint()* function to export the most performing model into the file: *ResNet50_v2_12_0.950.h5*.
#### - chest_xray-model folder
This is our final model format, we obtain it as output of method *tf_saved_model.save()*, applied to our *ResNet50_v2_12_0.950.h5* ; in this format it is compatible with *TF-Serving* service.
#### - image-model-dockerfile
This is the *docker* that we buil to apply the model.
We decided to have two separated services, one specialized in model application *model*, and another one that collect the requests from the client and provide to data elaboration pre and post evaluation *gateway*.
#### - tf-serving-connect.ipynb
Through this notebook we implemented the *gateway* service that provide image's pre-elaboration and send it to *image-model-dockerfile* that it is running to evaluate the x-ray chest images submitted.
#### - gateway.py
this is the convertion of the notebook *tf-serving-connect.ipynb* in a python script.
#### - Pipfile and Pipfile.lock
These files specify the dependencies that *gateway.py* script needs to install running in a virtual environment.
#### - proto.py
In this file we included the method *np_to_protobuf()*, this is the only method thatvwe need from *tensorflow* library.
In this way we can avoid to include in the project the huge *tensorflow* library (1.7Gb).
#### - image-gateway.dockerfile
This is the file to build the *docker* for the *gateway service*. We use this *dockerfile* to specify its parameters.
#### - test.py
This script provide the access at the diagnostic service, it loads the image url from the *user_terminal* and send it to the *gateway-service* receving back the image evaluation.
#### - docker-compose.yaml
This configuration file it is used to put the two docker in the same network and test the services using the *docker-compose* function.
#### - kube-config folder
This folder contains the *kuberenetes* configuration file that we will use in section_3.
#### - model-deployment.yaml
Configuration file for the model deployment.
#### - model-service.yaml
Configuration file for the model service.
#### - gateway-deployment.yaml
Configuration file for the gateway deployment.
#### - gateway-service.yaml
Configuration file for the gateway service.
#### - test_kuberenetes.py
Script to test our services deployed in a local kuberenetes

---

### Running the project:
#### Get a copy of project and dependencies, or clone the repository:
```
git clone https://github.com/ISENBECK66/X-NetMed
```

---

# Deployment 1 - Docker and flask 
## A local implementation!
---
#### Prerequisite :
---
- Install docker :
```
install docker
```
- Install virtual environment:
```
pip install pipenv
```
---
#### Terminal_1 - TF-Serving in a docker 
---
*TF-serving* Docker :
- Build docker:
```
docker build -t final-proj-model:resnet50-v2-001 -f image-model.dockerfile .
```
- Run docker:
```
docker run -it --rm -p 8500:8500 final-proj-model:resnet50-v2-001
```
---
#### Terminal_2 - Gateway as local service
---
Install dependencies in the virtual environment:
(Run it into the folder where Pipfile and Pipfile.lock are located)
``` 
pipenv install
```
- All the dependencies should be automatically soddisfied, just verify.
- Run the local service using gunicorn inside the virtual environment:
```
pipenv run gunicorn --bind 0.0.0.0:9696 gateway:app
```
---
#### Terminal_3 - TEST
---
```
python test_local.py
```
Warning : the url of the image it is *hardcoded* in the script, if you want to eavluate another image please modify the script before to run it.

---
# Deployment 2: docker-compose
## Run everything in dockers, almost ready for the cloud! 

---
#### Prerequisite:
---
- Install docker-compose:
```
install docker-compose
```
#### Terminal_1 - Docker-compose:
---
- Run the compose:
```
docker-compose up
```
---
#### Terminal_2 - Test:
---
```
python test.py
```
#####
Warning : the URL of an image of a chest in x-ray will be requested from *test.py* script.

Here you can find a set of URLs that you can use to test the service, otherwise you can upload your personal *chest x-ray image* and provide the URL to the script. 

https://github.com/ISENBECK66/ML2023/blob/main/NORMAL2-IM-0132-0001.jpeg?raw=true - (NORMALE)
https://github.com/ISENBECK66/ML2023/blob/main/NORMAL2-IM-0135-0001.jpeg?raw=true - (NORMALE)
https://github.com/ISENBECK66/ML2023/blob/main/person3_virus_15.jpeg?raw=true - (PNEUMONIA)
https://github.com/ISENBECK66/ML2023/blob/main/person1_virus_11.jpeg?raw=true - (PNEUMONIA)
#####

---
# Deployment 3 : Kubernetes
## Run dockers in the cloud with automatic scaling and management! 
---

#### Prerequisite:
---
##### Install docker:
```
install docker
```
##### Install kind: tool to set-up a local kuberenetes cluster
```
install kind
```
##### Install kubectl: tool for interacting with every kuberenetes cluster
```
install kubectl
```
---
#### Cluster management:
---
##### Create the cluster (default name kind):
```
kind create cluster
```
##### Show cluster information:
```
kubectl cluster-info --context kind-kind
```
---
#### Load dockers in the cluster:
---
```
kind load docker-image final-proj-model:resnet50-v2-001
```
```
kind load docker-image final-proj-gateway:001
```
---
#### Set up Deployments in the cluster:
---
```
cd kube-config
```
```
kubectl apply -f model-deployment.yaml
```
```
kubectl apply -f gateway-deployment.yaml
```
---
#### Set up Services in the cluster:
---
```
kubectl apply -f model-service.yaml
```
```
kubectl apply -f gateway-service.yaml
```
---
#### Verify Pods and Services status in the cluster:
---
```
kubectl get pod
```
```
kubectl get service
```
---
#### TEST the deployment - from a new terminal:
---
```
python test_kuberenetes.py
```
#####
Warning : the URL of an image of a chest in x-ray will be requested from *test_kuberenetes.py* script.

Here you can find a set of URLs that you can use to test the service, otherwise you can upload your personal *chest x-ray image* and provide the URL to the script. 

https://github.com/ISENBECK66/ML2023/blob/main/NORMAL2-IM-0132-0001.jpeg?raw=true - (NORMALE)
https://github.com/ISENBECK66/ML2023/blob/main/NORMAL2-IM-0135-0001.jpeg?raw=true - (NORMALE)
https://github.com/ISENBECK66/ML2023/blob/main/person3_virus_15.jpeg?raw=true - (PNEUMONIA)
https://github.com/ISENBECK66/ML2023/blob/main/person1_virus_11.jpeg?raw=true - (PNEUMONIA)
#####
