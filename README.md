# X-NetMed
A Neural Network approach to pneumonia identification in X-rays images

---

## 1 - Problem description

Not surprisingly many consider that chest radiology, which is a relatively inexpensive test, plays a fundamental and important role in the diagnosis of pneumonia, together with clinical assessment and sometimes appropriate microbiological testing. Its primary purpose is to diagnose or exclude pneumonia, but it will also show the extent of the pneumonia, the presence or absence of associated comorbid conditions or complications, all of which may act as prognostic indicators, and it can also be used for subsequent follow-up to check for resolution.

Certainly, in the case of patients admitted to hospital there is evidence that the early performance of a chest radiograph is associated with clinical benefit, including a significantly shorter hospital length of stay and antibiotic use after radiologyIt is possible for doctors to understand the presence of Pneumonia.

Pneumonia is an infection that affects one or both lungs. It causes the air sacs, or alveoli, of the lungs to fill up with fluid or pus. Bacteria, viruses, or fungi may cause pneumonia. 
Symptoms can range from mild to serious and may include a cough with or without mucus, fever, chills, and trouble breathing

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

The script *train.py* load the model : *player_model.bin* and it can run in a separate virtual environment across its dependency files *Pipenv* and *Pipenv.lock*.
*flask* was used for the local deployment in *train.py* script.

- Install pipenv :
```
pip install pipenv
```
- Get a copy of project and dependencies, or clone the repository :
```
git clone https://github.com/bergimax/footballer-value/
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
- If you edit the market values to analize some data, you should modify the parameters in the file test.py, maybe you cane take them from the smaller dataset present in this repo of each market:
```
vi test.py
```
P.S: The current values in test.py are taken from the dataset, raw number 2075.

---

#### Video of the service running :
I loaded a small video where you can see how the service works, everything it's in the 'Proof of working' folder.

The video show the local service starting in Docker and how it respond to the test.py
I also attached the screenshot of the service running with flask and gunicorn.
