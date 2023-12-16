# X-NetMed
![Screenshot](human-skull-x-ray-image.webp)

A Neural Network approach to pneumonia identification in X-rays images

---

## 1 - Scenario and problem description : *The importance of a precox diagnosis in pneumonia disease* 

Pneumonia is inflammation and fluid in your lungs caused by a bacterial, viral or fungal infection. It makes it difficult to breathe and can cause a fever and cough with yellow, green or bloody mucus. The flu, COVID-19 and pneumococcal disease are common causes of pneumonia. Treatment depends on the cause and severity of pneumonia.

Not surprisingly many consider that chest radiology, which is a relatively inexpensive test, plays a fundamental and important role in the diagnosis of pneumonia, together with clinical assessment and sometimes appropriate microbiological testing. Its primary purpose is to diagnose or exclude pneumonia.

Certainly, in the case of patients admitted to hospital there is evidence that the early performance of a chest radiograph is associated with clinical benefit, including a significantly shorter hospital length of stay and antibiotic use after radiologyIt is possible for doctors to understand the presence of Pneumonia.

---
## 2 - The Goal

The target of this project is to automatically evaluate the X-ray images, and provide a fast diagnosis in presence of a pneumonia infection.
We obtained this result trought a Neural Network and a pretrained model that it is been adapted for our scopes.

--- 

## 3 - Data

This dataset used for train the model come from Keggle and contains almost 6000 x-ray image splitted in classes:
[https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia]

---

## 4 - Structure of the repository

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
