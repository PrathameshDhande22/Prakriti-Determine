# Testing the NLP Chat bot Model
import json
import os
import random
from joblib import load
from nltk import WordNetLemmatizer, word_tokenize
import numpy as np

path = os.path.join("Models/nlpbot")
model = load(path)
words: list = load(os.path.join("Models/words"))
classes: list = load(os.path.join("Models/classes"))
intents = json.loads(open(os.path.join("intents.json"), "r").read())

print(words, classes)

sentence = "suggest me the diet"
sentence_words = word_tokenize(sentence)
lemmatizer = WordNetLemmatizer()

sentence_words = [lemmatizer.lemmatize(w) for w in sentence_words]
bag = [0] * len(words)
print(sentence_words)

for s in sentence_words:
    for i, w in enumerate(words):
        if w == s:
            bag[i] = 1
bag = np.array(bag)
print(bag)

results = model.predict(np.array([bag]))[0]
print(results)

index = np.argmax(results)
print("index : ", index)

max_prob = np.max(results)
print("Probability : ", max_prob)

tag = classes[index]
print("tag :", tag)

for intent in intents["intent"]:
    if intent["tag"] == tag:
        print(random.choice(intent["responses"]))
        break
