from sklearn.model_selection import train_test_split
import pandas as pd
from tensorflow import optimizers
from tensorflow import keras
from joblib import dump
import os
import logging
import sys
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
os.environ["TF_ENABLE_ONEDNN_OPTS"] = str(0)
# Initializing the logging module to log everything.
format = "%(asctime)s - %(filename)s - %(levelname)s - Line No : %(lineno)d - %(message)s"
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(fmt=format)
logger.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Importing the required Modules

logger.info("Training the prakriti Model")

logger.info("Reading the Prakriti Dataset")
PATH = os.getcwd()
df = pd.read_csv(f"{PATH}/dataset/data.csv")

logger.info("Separating the X and Y values from the dataset")
X = df.iloc[:, :-1].values
Y = df.iloc[:, 20].values

logger.info("Splitting the 80% training and 20% Testing dataset")
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2,random_state=32
)

logger.info("Creating the Model")
model = keras.Sequential(
    [
        keras.layers.Input(shape=(20,)),
        keras.layers.Dense(19, activation="relu"),
        keras.layers.Dense(300, activation="relu"),
        keras.layers.Dense(250, activation="relu"),
        keras.layers.Dense(200, activation="relu"),
        keras.layers.Dense(150, activation="relu"),
        keras.layers.Dense(100, activation="relu"),
        keras.layers.Dense(50, activation="relu"),
        keras.layers.Dense(45, activation="relu"),
        keras.layers.Dense(30, activation="relu"),
        keras.layers.Dense(20, activation="relu"),
        keras.layers.Dense(15, activation="relu"),
        keras.layers.Dense(6, activation="sigmoid"),
    ]
)

adam = optimizers.Adam()

logger.info("Compiling the Model")
model.compile(
    optimizer=adam, loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

logger.info("Training the Model Now.")
model.fit(X_train, y_train, epochs=25, batch_size=64, validation_split=0.2)

logger.info("Testing the Model with testing dataset")
y_predict = model.predict(X_test)

logger.info("Testing the Accuracy of the Model")
y_predict_labels = [np.argmax(i) for i in y_predict]
print("Accuracy : ", accuracy_score(y_test, y_predict_labels)*100, "%")
print("Confusion Matrix : \n", confusion_matrix(y_test, y_predict_labels))

logger.info("Dumping the Model as the object to Model Folder")
model.save(os.path.join("Models", "prakriti.keras"))

logger.info("Model has been Dumped Successfully.")
