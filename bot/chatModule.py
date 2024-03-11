import json
import os
import random
from typing import TypedDict
from joblib import load
from diet import recommend_Diet
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
    response: str | list
    tag: str


class ChatResponse(TypedDict):
    response: dict | str


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


async def saveEveryResponse(
    received: dict[str, str], chat, session: Session, tag: str
) -> None:
    newchat = chat(
        name=received["name"],
        message=received["message"],
        detected_tag=tag,
    )
    session.add(newchat)
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
confirm = False
recommend = False
prakriti = None


def clearAll(exclude=False) -> None:
    global ans_list, i, flag, confirm, recommend, prakriti
    ans_list.clear()
    i = -1
    flag = False
    confirm = False
    if not exclude:
        recommend = False
        prakriti = None


async def chatWithUser(msg: dict, Chat, session: Session) -> ChatResponse:
    global flag, limit, i, ans_list, confirm, recommend, prakriti
    try:
        if flag:
            if str(msg.get("message")).lower() == "yes" and not confirm:
                confirm = True
            elif not confirm:
                clearAll()
                return {"response": "Skipped Predicting the Prakriti"}
            if confirm:
                i += 1
                if i != 0:
                    try:
                        inputs = int(msg["message"])
                        if inputs < 3 and inputs >= 0:
                            ans_list.append(int(msg["message"]))
                        else:
                            i -= 1
                            logger.info("Input given rather than 0,1,2")
                    except ValueError as e:
                        logger.warn(f"other than input is given - {e}")
                        clearAll()
                        return {
                            "response": "OOPS! you not answered the question correctly quitting the questionare."
                        }
                print(ans_list)
                if limit <= i:
                    prakriti = get_ans(ans_list)
                    msg = f"Your Prakriti is {prakriti}"
                    clearAll(exclude=True)
                    recommend = True
                    return {
                        "response": [
                            msg,
                            {
                                "question": "Want Diet Recommendation based on Your Prakriti?",
                                "options": {0: "yes", 1: "no"},
                            },
                        ]
                    }
                return {"response": questions.get(i)}
        elif recommend:
            if str(msg.get("message")).lower() == "yes":
                diet = recommend_Diet(prakriti)
                clearAll()
                return {"response": diet}
            else:
                clearAll()
                return {"response": "Skipped Diet Recommendation"}
        else:
            reply: Response = getResponseChat(msg["message"])
            print(f"tag => {reply['tag']} , message => {reply['response']}")
            if reply["tag"] == "prakriti":
                flag = True
                resp = [
                    reply.get("response"),
                    {
                        "question": "Answer Yes to get Started",
                        "options": {0: "yes", 1: "no"},
                    },
                ]
                reply["response"] = resp
            await saveEveryResponse(msg, Chat, session, reply["tag"])
            return reply
    except Exception as e:
        logger.error(f"Exception occured while chatting - {e}")
