# X-NetMed, or: 
## *A Neural Network approach to pneumonia identification in X-rays images*
![Screenshot](human-skull-x-ray-image.webp)
---
### The importance of a precox diagnosis in pneumonia disease :

####
Pneumonia is inflammation and fluid in your lungs caused by a bacterial, viral or fungal infection. It makes it difficult to breathe and can cause a fever and cough with yellow, green or bloody mucus. The flu, COVID-19 and pneumococcal disease are common causes of pneumonia. Treatment depends on the cause and severity of pneumonia.
Not surprisingly many consider that chest radiology, which is a relatively inexpensive test, plays a fundamental and important role in the diagnosis of pneumonia, together with clinical assessment and sometimes appropriate microbiological testing. Its primary purpose is to diagnose or exclude pneumonia.
Certainly, in the case of patients admitted to hospital there is evidence that the early performance of a chest radiograph is associated with clinical benefit, including a significantly shorter hospital length of stay and antibiotic use after radiologyIt is possible for doctors to understand the presence of Pneumonia.
####
---
### Neural Network and Deep Learning to build a binary classifier to elaborate x-ray images :
####
The target of this project is to automatically verify the presence of a a pneumonia infection throught the analisys of the x-ray images of the patient's chest.
We used a Neural Network and a pretrained model that it is been adapted for our scopes.
The choosen pre-trained model it has been *ResNet50* from *keras* package.
The initial weights for the preprocess of the images has come from *imagenet*.
####
--- 
### Dataset :
####
The *dataset* that is been used for train our model come from *Keggle* and contains almost 6000 x-ray images splitted in *NORMAL* and *PNEUMONIA* classes:
[https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia]
####
---
### Repository :
#### notebook.ipynb file
This repository contains *notebook.ipynb file* : In this file we load the *ResNet50* model and the *dataset* downloaded from kaggle.
We worked on the *model* building on its top our specific *dense layer / inner layer* trained on the images loaded from our *dataset*.     
In the same file we tried different setup to obtain the best performance, tuning model parameters, as : *leraning_rate*, *drop_rate* and *augmentation*.
#### ResNet50_v2_12_0.950.h5 file
We used the *keras.callbacks.ModelCheckpoint()* function to export the most performing model into the file: *ResNet50_v2_12_0.950.h5*
#### chest_xray-model folder



### DATASET
- **chest_xray_small**: this folder contains the x-ray images used for the training

### Files
- **Proj1.ipynb**: 
- **Pipfile and Pipfile.lock**: contains the dependencies to run the repo
- **predict.py**: contains the prediction using flask
- **test.py**: contains some values to test the model
- **player_model.bin**: this is the model got from the train.py using Pickle
- **train.py**: contains the model with the best performance in the testing set, obtained using the notebook
- **Dockerfile**: contains the image for the docker

---
## 5 - Loading final model into a service:

#### pipenv 

The script *train.py* load the model : *r_model.bin* and it can run in a separate virtual environment across its dependency files *Pipenv* and *Pipenv.lock*.
*flask* was used for the local deployment in *train.py* script.

- Install pipenv :
```
pip install pipenv
```
- Get a copy of project and dependencies, or clone the repository :
```
git clone https://github.co/
```
- From the project's folder, run :
``` 
pipenv install
```
- All the dependencies should be automatically soddisfied, just verify.
- Run the local service using gunicorn inside the virtual environment:
```
pipenv run gunicorn --bind 0.0.0.0:9696 predict:app
```

#### Docker
There is also the file: *Dockerfile* in the repository, through this you can run the service in a completely separate container. To run the Docker, be sure your docker service is running. If you are using wsl2 on Windows, to run the build command you need to make sure your docker dekstop is running, otherwise you will get an error. 
For the docker, you have to:

- From the project directory, create the docker image :
```
docker build -t player_prediction .
```
- Run the docker image created:
```
docker run -it --rm -p 9696:9696 player_prediction:latest
```
The build command can take several minutes to run. Just give it time.

#### Test the local service:

- To test the local service, you can run the test script in another terminal:
```
python test.py
```
- If you e market:
```
vi test.py
```
---

#### Video of the service running :
I also attached the screenshot of the service running with flask and gunicorn.
