import json
import os
import random
from threading import Thread

import numpy as np
from joblib import load
from nltk import WordNetLemmatizer, word_tokenize
from sqlalchemy.orm import Session

from database import Chat, Prakriti
from diet import recommend_Diet
from logger import logger
from models import ChatResponse, Intents, PrakritBotResponse, Reply, Response
from question import questions
from keras.models import load_model

os.environ["TF_ENABLE_ONEDNN_OPTS"] = str(0)
chatBot_Model = load_model(os.path.join("Models", "nlpbot.keras"))
words: list = load(os.path.join("Models/words"))
classes: list = load(os.path.join("Models/classes"))
prakriti_Model = load_model(os.path.join("Models", "prakriti.keras"))
intents: Intents = json.loads(open(os.path.join("intents.json"), "r").read())
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


def getResponseChat(msg: str) -> Response:
    tag = getResponseTag(msg)
    for intent in intents["intent"]:
        if intent["tag"] == tag:
            return {"response": random.choice(intent["responses"]), "tag": tag}


def saveData(ans: list[int], session: Session) -> None:
    data = {
        "body_size": "",
        "body_width": "",
        "height": "",
        "bone_structure": "",
        "complexion": "",
        "general_feel_of_skin": "",
        "texture_of_skin": "",
        "hair_color": "",
        "appearance_of_hair": "",
        "shape_of_face": "",
        "eyes": "",
        "eyelashes": "",
        "blinking_of_eyes": "",
        "cheeks": "",
        "nose": "",
        "teeth_and_gums": "",
        "lips": "",
        "nails": "",
        "appetite": "",
        "liking_tastes": "",
        "dosha": ""
    }
    for i, k in enumerate(list(data.keys())):
        data[k] = ans[i]
    par = Prakriti(**data)
    session.add(par)
    session.commit()
    logger.info("Saved the Data to DB")


async def saveEveryResponse(
    received: Reply, session: Session, tag: str
) -> None:
    newchat = Chat(
        name=received["name"],
        message=received["message"],
        detected_tag=tag,
    )
    session.add(newchat)
    session.commit()


def get_ans(ans: list[int]) -> PrakritBotResponse:
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
    return PrakritBotResponse(index, praks.get(index))


limit: int = len(questions)
i: int = -1
flag = False
ans_list: list = []
confirm: bool = False
recommend: bool = False
prakriti: PrakritBotResponse = None
already_known: str = str()
ask_Known: bool = False
start_questionaire: bool = False
count_wrong: int = 0


def clearAll(exclude: bool = False) -> None:
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


def askQuestion(msg: Reply, session: Session) -> dict | str:
    global recommend, ans_list, prakriti, start_questionaire, i, limit, already_known, ask_Known
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
            msg = f"Your Prakriti is <b>{prakriti.prakriti}</b>"
            if prakriti.prakriti.lower().strip() == already_known and ask_Known:
                ans_list.append(int(prakriti.index))
                Thread(target=saveData, args=(ans_list, session)).start()
                clearAll()
                return [
                    msg,
                    "Thank you for taking the time to answer some questions. Your responses will greatly assist me in improving my accuracy.",
                ]
            elif ask_Known and prakriti.prakriti.lower().strip() != already_known:
                clearAll(exclude=True)
                recommend = True
                return [
                    msg,
                    f"The input you provided is <b>{already_known.title()}</b> and our model predicted as <b>{prakriti.prakriti.title()}</b> is different.",
                    "It seems that there may be one or more incorrect answers to the questions you provided. Please review and verify your responses.",
                    {
                        "question": "Want Diet Recommendation based on Your Prakriti?",
                        "options": {0: "yes", 1: "no"},
                    },
                ]
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


def handleWrongAnswer(response: str | dict | list) -> ChatResponse:
    global count_wrong
    count_wrong += 1
    if count_wrong < 3:
        return {"response": response}
    else:
        clearAll()
        return {
            "response": "Exiting the Questionaire as You have not given the Proper Input"
        }


async def chatWithUser(msg: Reply, session: Session) -> ChatResponse:
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
                    return {"response": askQuestion(msg, session)}
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
                                        f"Your Response has been recorded as <b>{already_known.title()}</b>",
                                        "Please provide the answer to the following question to enhance my accuracy. I will then use your response for analysis.",
                                        askQuestion(msg, session),
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
                                    askQuestion(msg, session),
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
                diet = recommend_Diet(prakriti.prakriti)
                diet.append(
                    "Thank You For predicting Prakriti with <b>AYURBOT</b>")
                clearAll()
                return {"response": diet}
            else:
                clearAll()
                return {"response": ["Skipped Diet Recommendation", "Thank You For predicting Prakriti with <b>AYURBOT</b>"]}
        else:
            reply: Response = getResponseChat(msg["message"])
            print(f"tag => {reply['tag']} , message => {reply['response']}")
            if reply["tag"] == "prakriti":
                flag = True
                resp = [
                    reply.get("response"),
                    "<b>NOTE</b>: Click on Exclamation Mark at the Right hand side of the each Question to Know the Explanation of the asked Question and Options.",
                    {
                        "question": "Answer Yes to get Started?",
                        "options": {0: "yes", 1: "no"},
                    },
                ]
                reply["response"] = resp
            await saveEveryResponse(msg, session, reply["tag"])
            return reply
    except Exception as e:
        clearAll()
        logger.error(f"Exception occured while chatting - {e}")
