import json
import os
import random
from typing import TypedDict
from joblib import load
from question import questions
from nltk import WordNetLemmatizer, word_tokenize
import numpy as np
from sqlalchemy.orm import Session
from logger import logger

os.environ["TF_ENABLE_ONEDNN_OPTS"] = str(0)
chatBot_Model = load(os.path.join("Models/nlpbot"))
words: list = load(os.path.join("Models/words"))
classes: list = load(os.path.join("Models/classes"))
prakriti_Model = load(os.path.join("Models/prakriti"))
intents = json.loads(open(os.path.join("intents.json"), "r").read())
lemmatizer = WordNetLemmatizer()


class Response(TypedDict):
    response: str
    tag: str


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


def getResponseChat(msg: str) -> Response:
    tag = getResponseTag(msg)
    for intent in intents["intent"]:
        if intent["tag"] == tag:
            return {"response": random.choice(intent["responses"]), "tag": tag}


def saveEveryResponse(
    received: dict[str, str], chat, session: Session, tag: str
) -> None:
    newChat = chat(
        name=received["name"],
        message=received["message"],
        detected_tag=tag,
    )
    session.add(newChat)
    session.commit()


def get_ans(ans: list) -> str:
    val = prakriti_Model.predict(np.array([ans]))
    index = np.argmax(val)
    praks = {
        0: "Vata",
        1: "Pitta",
        2: "Kapha",
        3: "Vata - Pitta",
        4: "Vata - Kapha",
        5: "Pitta - Kapha",
    }
    return praks.get(index)


limit = len(questions)
i = -1
flag = False
ans_list = []


async def chatWithUser(msg: dict, Chat, session: Session) -> dict:
    global flag, limit, i, ans_list
    try:
        if flag:
            i += 1
            if i != 0:
                try:
                    ans_list.append(int(msg["message"]))
                except ValueError as e:
                    logger.warn(f"other than input is given - {e}")
                    ans_list.clear()
                    flag = False
                    i = 0
                    return {
                        "response": "OOPS! you not answered the question correctly quitting the questionare."
                    }

            print(ans_list)
            if limit <= i:
                prakriti = get_ans(ans_list)
                i = 0
                ans_list.clear()
                flag = False
                return {"response": f"Your Prakriti is {prakriti}"}
            return {"response": questions.get(i)}
        else:
            reply: Response = getResponseChat(msg["message"])
            print(f"tag => {reply['tag']} , message => {reply['response']}")
            if reply["tag"] == "prakriti":
                flag = True
            saveEveryResponse(msg, Chat, session, reply["tag"])
            return reply
    except Exception as e:
        logger.error(f"Exception occured while chatting - {e}")
