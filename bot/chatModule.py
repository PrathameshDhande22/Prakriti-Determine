import json
import os
import random
import pandas as pd
from joblib import load
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from question import questions

# loading the dumped model
PATH = os.getcwd()
model = load(rf"{PATH}\Models\nlm")
prakrit_model = load(rf"{PATH}\Models\prakriti")

# Importing the Sentence intent .csv file
df = pd.read_csv(f"{PATH}\dataset\sentences_intent.csv")

# Importing the json file for getting the responses
with open(f"{PATH}\intents.json", "r") as f:
    intents = json.loads(f.read())["intent"]

cvc = CountVectorizer(min_df=1)
X_train = df.Sentence

labels = {
    5: "greeting",
    4: "goodbye",
    10: "thanks",
    0: "about",
    7: "name",
    6: "help",
    8: "noanswer",
    9: "prakriti",
    3: "creators",
    2: "badwords",
    1: "acknowledge",
}

cvc.fit(X_train.values)


def get_tag(msg_list) -> str:
    index_no = np.argmax(model.predict(msg_list))
    return labels.get(index_no)


def get_ans(ans) -> str:
    val = prakrit_model.predict(ans).item()
    praks = {
        0: "vata",
        1: "pitta",
        2: "kapha",
        3: "vata+pitta",
        4: "vata+kapha",
        5: "pitta+kapha",
    }
    return praks.get(val)


msg_list = []

flag = False
i = 0
lis = []
limit = len(questions.items())


def get_responses(msg: str) -> str:
    global flag, i, lis, limit
    if flag:
        if i != 0:
            try:
                if int(msg) > 4:
                    ans = "<strong>Wrong Answer</strong>"
                    flag = False
                    return ans
                lis.append(int(msg) - 1)
            except ValueError as v:
                flag = False
                return "<strong>Wrong Answer</strong>"

        ans = questions.get(i)
        if i == limit:
            flag = False
            i = 0
            praki = get_ans([lis])
            ans = f"<p><strong>Your Prakriti is:</strong></p> {praki}"

        i = i + 1
        print("ans => ", lis, flag)
        return ans

    tag = get_tag(cvc.transform([msg]))
    if tag == "prakriti":
        flag = True
    for intent in intents:
        if tag == intent["tag"]:
            return random.choice(intent["responses"])
