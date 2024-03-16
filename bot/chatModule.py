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
already_known = str()
ask_Known = False
start_questionaire = False
count_wrong = 0


def clearAll(exclude=False) -> None:
    global ans_list, i, flag, confirm, recommend, prakriti, already_known, ask_Known, start_questionaire, count_wrong
    ans_list.clear()
    i = -1
    flag = False
    confirm = False
    ask_Known = False
    start_questionaire = False
    count_wrong = 0
    if not exclude:
        ask_Known = False
        already_known = str()
        recommend = False
        prakriti = None


def askQuestion(msg):
    global recommend, ans_list, prakriti, start_questionaire, i, limit
    if start_questionaire:
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
                return "<b>OOPS!</b> you have not answered the question correctly quitting the questionare."
        print(ans_list)
        if limit <= i:
            prakriti = get_ans(ans_list)
            msg = f"Your Prakriti is <b>{prakriti}</b>"
            clearAll(exclude=True)
            recommend = True
            return [
                msg,
                {
                    "question": "Want Diet Recommendation based on Your Prakriti?",
                    "options": {0: "yes", 1: "no"},
                },
            ]

        return questions.get(i)


def handleWrongAnswer(response):
    global count_wrong
    count_wrong += 1
    if count_wrong < 3:
        return {"response": response}
    else:
        clearAll()
        return {
            "response": "Exiting the Questionaire as You have not given the Proper Input"
        }


async def chatWithUser(msg: dict, Chat, session: Session) -> ChatResponse:
    global flag, limit, i, ans_list, confirm, count_wrong, recommend, prakriti, already_known, ask_Known, start_questionaire
    try:
        if flag:
            umessage = str(msg.get("message")).lower().strip()
            if (
                umessage == "quit"
                or umessage == "exit"
                or "exit" in umessage
                or "quit" in umessage
            ):
                clearAll()
                return {
                    "response": "Exiting from the Process, Thank you 🙏🙏 for using me."
                }
            if umessage == "yes" and not confirm:
                count_wrong = 0
                confirm = True
                return {
                    "response": {
                        "question": "Do you already know your Prakriti? If yes, could you please share it with me?",
                        "options": {0: "yes", 1: "no"},
                    }
                }
            elif not confirm and umessage == "no":
                clearAll()
                return {"response": "Skipped Predicting the Prakriti"}
            elif not confirm:
                return handleWrongAnswer(
                    [
                        "Give Proper Input either <code>yes</code> or <code>no</code>",
                        {
                            "question": "Answer Yes to get Started?",
                            "options": {0: "yes", 1: "no"},
                        },
                    ]
                )
            elif confirm:
                if start_questionaire:
                    return {"response": askQuestion(msg)}
                else:
                    userMessage = str(msg.get("message")).lower().strip()
                    prakriti_types = [
                        "vata",
                        "pitta",
                        "kapha",
                        "vata - pitta",
                        "vata - kapha",
                        "pitta - kapha",
                    ]
                    if ask_Known:
                        if userMessage in prakriti_types:
                            already_known = userMessage
                            start_questionaire = True
                            if start_questionaire:
                                return {
                                    "response": [
                                        f"Your Response has been recorded as <b>{already_known}</b>",
                                        "Please provide the answer to the following question to enhance my accuracy. I will then use your response for analysis.",
                                        askQuestion(msg),
                                    ]
                                }
                        else:
                            return handleWrongAnswer(
                                [
                                    "Select from above Input",
                                    {
                                        "question": "What is Your Prakriti",
                                        "options": {
                                            0: "Vata",
                                            1: "Pitta",
                                            2: "Kapha",
                                            3: "Vata - Pitta",
                                            4: "Vata - Kapha",
                                            5: "Pitta - Kapha",
                                        },
                                    },
                                ]
                            )

                    elif userMessage == "yes" and not ask_Known:
                        ask_Known = True
                        count_wrong = 0
                        return {
                            "response": [
                                "Thank you for taking the time to share your Prakriti with me! Your input is invaluable and will greatly assist me in providing you with more personalized recommendations.",
                                {
                                    "question": "What is Your Prakriti",
                                    "options": {
                                        0: "Vata",
                                        1: "Pitta",
                                        2: "Kapha",
                                        3: "Vata - Pitta",
                                        4: "Vata - Kapha",
                                        5: "Pitta - Kapha",
                                    },
                                },
                            ]
                        }

                    elif not ask_Known and userMessage == "no":
                        start_questionaire = True
                        if start_questionaire:
                            return {
                                "response": [
                                    "Answer the Above Set of Questions to Predict Your Prakriti",
                                    askQuestion(msg),
                                ]
                            }
                    else:
                        return handleWrongAnswer(
                            [
                                "Please give Proper Input Either Yes or No",
                                {
                                    "question": "Do you already know your Prakriti? If yes, could you please share it with me?",
                                    "options": {0: "yes", 1: "no"},
                                },
                            ]
                        )

        elif recommend:
            if str(msg.get("message")).lower().strip() == "yes":
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
                        "question": "Answer Yes to get Started?",
                        "options": {0: "yes", 1: "no"},
                    },
                ]
                reply["response"] = resp
            await saveEveryResponse(msg, Chat, session, reply["tag"])
            return reply
    except Exception as e:
        clearAll()
        logger.error(f"Exception occured while chatting - {e}")
