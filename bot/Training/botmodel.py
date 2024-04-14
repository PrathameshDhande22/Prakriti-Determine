import pandas as pd
from nltk.stem import WordNetLemmatizer
import nltk
import json
import numpy as np
from keras.optimizers import SGD
from keras.models import Sequential
from keras.layers import Dense, Dropout, Input
import random
import logging
import os
from joblib import dump
os.environ["TF_ENABLE_ONEDNN_OPTS"] = str(0)
logging.basicConfig(
    format="%(asctime)s - %(filename)s - %(levelname)s - Line No : %(lineno)d - %(message)s",
    level=logging.INFO,
)

# Importing the required Modules

logging.info("Starting the Chatbot Model Training")

logging.info("Initializing the Lemmatizer")
lemmatizer = WordNetLemmatizer()

logging.info("Downloading the required packages for NLP")
nltk.download("omw-1.4")
nltk.download("punkt")
nltk.download("wordnet")

words = []
classes = []
documents = []
ignore_words = ["?", "!", ","]

logging.info("Reading the Intents.json File")
data_file = open(os.path.join("intents.json")).read()
intents: dict[str, list] = json.loads(data_file)

logging.info("Tokenizing the each pattern in the intents.json file")
for intent in intents["intent"]:
    for pattern in intent["patterns"]:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

logging.info("removing the words which doesn't mean anything")
words = [lemmatizer.lemmatize(w.lower())
         for w in words if w not in ignore_words]

logging.info("Sorting words, classes and documents")
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique lemmatized words", words)

logging.info("Dumping the words and classes as an binary object")
dump(words, os.path.join("Models/words"))
dump(classes, os.path.join("Models/classes"))

logging.info("Initiating the Training data")
training = []
output_empty = [0] * len(classes)
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(
        word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

logging.info("Training Dataset has been Created")

logging.info("Creating the training dataset and saving it.")
dataset = {}
for w in words:
    dataset[w] = []
dataset["tag"] = []
for train in training:
    for w, value in list(zip(words, train[0])):
        dataset[w].append(value)
    dataset["tag"].append(classes[np.argmax(train[1])])
index = []
for docu in documents:
    index.append(" ".join(docu[0]))
df = pd.DataFrame(dataset, index=index)
df.to_csv(os.path.join("dataset/sentences.csv"))

random.shuffle(training)
training_data = np.array(training, dtype=object)

logging.info("Extracting the X and Y values from the training data")
train_x = list(training_data[:, 0])
train_y = list(training_data[:, 1])

logging.info("Initializing the Keras Model")
model = Sequential()
model.add(Input(shape=(len(train_x[0]),)))
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))

logging.info("Compiling the Model")
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy",
              optimizer=sgd, metrics=["accuracy"])

logging.info("Training the Model with X and Y data")
model.fit(np.array(train_x), np.array(train_y),
          epochs=200, batch_size=5, verbose=1)

logging.info("Model has been Trained")
logging.info("dumping the Model")

model.save(os.path.join("Models", "nlpbot.keras"))
logging.info("Model has been Dumped Successfully")
