# X-NetMed, or: 
## *a Neural Network approach to pneumonia identification in X-rays images*
<img src="https://github.com/ISENBECK66/X-NetMed/blob/main/NORMAL2-IM-0132-0001.jpeg" width="300" height="300"> <img src="https://github.com/ISENBECK66/X-NetMed/blob/main/NORMAL2-IM-0132-0001.jpeg" width="300" height="300"> 



---

### The importance of a praecox pneumonia infection's diagnosis:

####
Pneumonia is an inflammation in your lungs caused by a bacterial, viral or fungal infection that makes difficult to breathe and can cause a fever and cough with yellow, green or bloody mucus. The flu, COVID-19 and pneumococcal disease are common causes of pneumonia. Treatment depends on the cause and severity of pneumonia. Not surprisingly many consider that chest radiology, which is a relatively inexpensive test, plays a fundamental and important role in the diagnosis of pneumonia, together with clinical assessment and (sometimes) appropriate microbiological testing. The primary purpose of chest radiology is to diagnose or exclude pneumonia.

####
---
### Neural Network and Deep Learning - a binary classification for chest x-ray images:
####
The target of this project is to use Deep Learning to create a service that automatically verify the presence of a pneumonia infection, processing the x-ray images of patients's chest.
On the base layer of a pretrained image classification model I built a new top layer, that has been trained to serve our scopes through a Neural Network.
The choosen pre-trained model is *ResNet50* from the *keras* package.
The initial weights in the preprocess model are coming from *imagenet*.

####
--- 
### Dataset:
####
The *dataset* used for the training of the model come from *Keggle* and contains ~ 6000 x-ray images, splitted in *NORMAL* and *PNEUMONIA* classes.
Here you can find all the information about the dataset :
[https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia]
####
---
### Software architecture :
I decided to develop two services, once for each main function:

#### Service 1 - *Gateway*:
- 1 This function load the input, an x-ray image, from an URL that is provided from the user through the user interface.
- 2 Execute a specific preprocessing on the image.
- 3 Send the data obtained trought the network to the *TF-Serving* service.
- 4 Wait the evaluation coming back from *TF-Serving*
- 5 Execute a post elaboration to present the results back to the user.
  
#### Service 2 - TF-Serving: 
- 1 This service take a preprocessed image as an input, coming from *Gateway* service.
- 2 The main task of this service it is to apply inference on the received data, using the model that we trained for this scope.
  
  *TF-Service use a lot of GPU resources to evaluate the image, and this is one of the main reason behind the choice to split the application in two different services*
  
- 3 Send back to *gateway* service the results of the elaboration.

---

### Software architecture :

```mermaid
sequenceDiagram
    Actor User
    box rgb(33,66,99) Service_1
    participant Gateway
    end
    box rgb(33,66,99) Service_2
    participant TF-Serving
    end
    User->>Gateway: image URL
    Gateway->>TF-Serving: preprocessed image
    TF-Serving->>TF-Serving: model
    TF-Serving->>Gateway: evaluation
    Gateway->>User: postprocessed evaluation 
```
---
### Repository content:
#### - notebook.ipynb file
In this file we load the *ResNet50* model and the *dataset* downloaded from kaggle.
We worked on the *model* building on its top our specific *dense layer / inner layer* trained on the images loaded from our *dataset*.     
In the same file we tuned the model parameters: *leraning_rate*, *drop_rate* and *augmentation* to obtain the best performances, and exported the best model we obtained in a h5 file.
#### - ResNet50_v2_12_0.950.h5 file
We used the *keras.callbacks.ModelCheckpoint()* function to export the most performing model into the file: *ResNet50_v2_12_0.950.h5*.
#### - chest_xray-model folder
This is the final format of the model, we obtained it as output of method *tf_saved_model.save()*, applied to our *ResNet50_v2_12_0.950.h5* ; in this format the model it is compatible with *TF-Serving* service.
#### - image-model-dockerfile
We use this file to build the *docker* running the *TF-Serving* service.
#### - tf-serving-connect.ipynb
Through this notebook we implemented the *gateway* service.
#### - gateway.py
This is the convertion of the notebook *tf-serving-connect.ipynb* in a python script.
#### - Pipfile and Pipfile.lock
These files specify the dependencies that *gateway.py* script needs to be installed and run in a virtual environment.
#### - proto.py
In this file we have the method *np_to_protobuf()*, in this way we can avoid to include in the project the huge *tensorflow* library (1.7Gb).
#### - test_local.py
Script to test deployment_1 : *gateway* running in a virtual environment and *TF-Serving* in a docker
#### - image-gateway.dockerfile
We use this file to build the *docker* running the *gateway* service.
#### - docker-compose.yaml
This configuration file it is used to put the two docker in the same network and test the services using the *docker-compose* function.
#### - test.py
Script to test deployment_2 : two services running in two dockers in one docker-compose
#### - kube-config folder
This folder contains the *kuberenetes* configuration file that we will use in section_3.
#### - kube-config/model-deployment.yaml
Configuration file for the model deployment.
#### - kube-config/model-service.yaml
Configuration file for the model service.
#### - kube-config/gateway-deployment.yaml
Configuration file for the gateway deployment.
#### - kube-config/gateway-service.yaml
Configuration file for the gateway service.
#### - test_kuberenetes.py
Script to test deployment_3 : two services deployed in a local cloud.

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

- Make sure to have properly installed : *docker* and *pipenv*:

---
#### Terminal_1 - TF-Serving in a docker 
---
Open a terminal in the main folder of the project.

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
Open a new terminal in the main folder of the project.

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

Open a new terminal in the main folder of the project.
Run the test script:
```
python test_local.py
```
Warning : the url of the image it is *hardcoded* in the script, if you want to eavluate another image please modify the script before to run it.
URL hardcoded : https://github.com/ISENBECK66/ML2023/blob/main/person3_virus_15.jpeg?raw=true

---
# Deployment 2: docker-compose
## Run everything in dockers, almost ready for the cloud! 

---
#### Prerequisite:
---

- Make sure to have properly installed : *docker* and *docker-compose*:

---
#### Terminal_1 - Dockers set up and compose 
---

Open a new terminal in the main folder of the project.

- Build *TF-serving* docker:
```
docker build -t final-proj-model:resnet50-v2-001 -f image-model.dockerfile .
```
- Build *Gateway* docker:
```
docker build -t final-proj-gateway:001 -f image-gateway.dockerfile .
```
- Run the compose:
```
docker-compose up
```
---
#### Terminal_2 - Test:
---
Open a new terminal in the main folder of the project.
Run the test script:
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

- Make sure to have properly installed : *docker*, *kind* and *kubectl*.

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
#### Load docker images into the cluster:
---

Open a terminal in the main folder of the project

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
#### Port forward :
---
```
kubectl port-forward service/gateway 8080:80
```
---
#### TEST the deployment:
---
Open a new terminal in the main folder of the project.
Rum the Test script:
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
