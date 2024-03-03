import json
import os
import random
from joblib import load
from question import questions
from nltk import WordNetLemmatizer, word_tokenize
import numpy as np
from sqlalchemy.orm import Session

os.environ["TF_ENABLE_ONEDNN_OPTS"] = str(0)
chatBot_Model = load(os.path.join("Models/nlpbot"))
words: list = load(os.path.join("Models/words"))
classes: list = load(os.path.join("Models/classes"))
prakriti_Model = load(os.path.join("Models/prakriti"))
intents = json.loads(open(os.path.join("intents.json"), "r").read())
lemmatizer = WordNetLemmatizer()


def getResponseTag(msg: str) -> str:
    sentence_words = word_tokenize(msg)
    sentence_words = [lemmatizer.lemmatize(w) for w in sentence_words]
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    bag = np.array(bag)
    results = chatBot_Model.predict(np.array([bag]))[0]
    index = np.argmax(results)
    return classes[index]


def getResponseChat(msg: str) -> dict[str, str]:
    tag = getResponseTag(msg)
    for intent in intents["intent"]:
        if intent["tag"] == tag:
            return {"response": random.choice(intent["responses"]), "tag": tag}


def saveEveryResponse(
    received: dict[str, str], Chat, session: Session, tag: str
) -> None:
    newChat = Chat(
        name=received["name"],
        message=received["message"],
        detected_tag=tag,
    )
    session.add(newChat)
    session.commit()


def get_ans(ans) -> str:
    # val = prakrit_model.predict(ans).item()
    praks = {
        0: "vata",
        1: "pitta",
        2: "kapha",
        3: "vata+pitta",
        4: "vata+kapha",
        5: "pitta+kapha",
    }
    # return praks.get(val)
