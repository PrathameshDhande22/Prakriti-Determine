from joblib import load
from sklearn.feature_extraction.text import CountVectorizer
import json
import random
import json
import random
import numpy as np
import pandas as pd
nl_model = load('./models/nlm')

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("./datasets/bodyfind.csv")

X = df.drop('Dosha', axis ='columns')
y = df['Dosha']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2);

model = RandomForestClassifier()
model.fit(X_train,y_train)

with open('intents.json', 'r') as f:
    intents = json.load(f)

intentList = {
    2: 'greeting',
    1: 'goodbye',
    6: 'thanks',
    0: 'about',
    4: 'name',
    3: 'help',
    5: 'prakriti'
}

df = pd.read_csv("./datasets/sentences_intent.csv")
X_train=df.Sentence

def get_intent(msg_count):
    ans = np.argmax(nl_model.predict(msg_count,verbose = 0))
    return intentList.get(ans)

vectorizer = CountVectorizer(min_df=1)
vectorizer.fit(X_train.values)
print(len(X_train.values))

questions={
    0:"<p><strong>What is the appearance of hair?</strong></p><p>1. Dry,Black, knotted, brittle</p><p>2. Straight, oily</p><p>3. Thick, curly</p>",
    # 0:'What is your body size? <br> Slim<br>Medium<br>Large',
    1:'<p><strong>What is your body weight?</strong><br /> 1. Low- difficulties in gaining weight<br /> 2.Moderate- no difficulties in gaining or losing weight<br /> 3.Heavy- difficulties in losing weight</p>',
    2:'<p><strong>What is your height?</strong><br /> 1.Short<br /> 2.Average<br /> 3.Tall</p>',
    3:'<p><strong>What is your bone structure?</strong><br /> 1.Light, Small- prominent joints<br /> 2.Medium, bone structure<br /> 3.Large - broad shoulders , heavy bone structure</p> ',
    4:'<p><strong>What is your complexion?</strong><br /> 1.Dark-tans easily<br /> 2.Fair- sunburns easily<br /> 3.White- pale, tans easily</p>',
    5:'<p><strong>Describe the general feel of skin-</strong><br /> 1.Dry and thin- cool to touch, rough<br /> 2.Smooth and warm, oily T-zone<br /> 3.Thick and moist-greasy, cold</p> ',
    6:'<p><strong>Describe the skin texture:</strong><br /> 1.Dry, pigments and aging<br /> 2.Freckles, many moles, redness and rashes<br /> 3.Oily</p> ',
    7:'<p><strong>What is your hair colour?</strong><br /> 1.Black/Brown,dull<br /> 2.Red, light brown, yellow<br /> 3.Brown</p>',
    8:'<p><strong>Describe the appearance of your hair:</strong></p> <p>1.Dry, black, knotted, brittle</p <p>2.Straight, oily</p> <p>3.Thick, curly</p>',
    9:'<p><strong>Describe the shape of face:</strong></p> <p>1.Long, angular, thin</p> <p>2.Heart-shaped, pointed chin</p> <p>3.Large, round, full</p>',
    10:'<p><strong>Describe your eyes:</strong></p> <p>1.Small, active, darting, dark eyes</p> <p>2.Medium-sized, penetrating, light-sensitive eyes</p> <p>3.Big, round, beautiful, glowing eyes</p> ',
    11:'<p><strong>Describe your eyelashes:</strong></p><p>1.Scanty eyelashes</p><p>2.Moderate eyelashes</p><p>3.Thick/Fused eyelashes</p>',
    12:'<p><strong>How often do you blink your eyes?</strong></p> <p>1.Excessive Blinking</p> <p>2.Moderate Blinking</p> <p>3.More or less stable</p>',
    13:'<p><strong>How are your cheeks?</strong></p> <p>1.Wrinkled, Sunken</p> <p>2.Smooth, Flat</p> <p>3.Rounded, Plump</p>',
    14:'<p><strong>How is your nose?</strong></p> <p>1.Crooked, Narrow</p> <p>2.Pointed, Average</p> <p>3.Rounded, Large open nostrils</p>',
    15:'<p><strong>Describe your teeth and gums:</strong></p> <p>1.Irregular, Protruding teeth, Receding gums</p> <p>2.Medium-sized teeth, Reddish gums</p> <p>3.Big, White, Strong teeth, Healthy gums</p>',
    16:'<p><strong>How are your lips?</strong></p> <p>1.Tight, thin, dry lips which chaps easily</p> <p>2.Lips are soft, medium-sized</p> <p>3.Lips are large, soft, pink, and full</p>',
    17:'<p><strong>How are your nails?</strong></p> <p>1.Dry, Rough, Brittle, Break</p> <p>2.Sharp, Flexible, Pink, Lustrous</p> <p>3.Thick, Oily, Smooth, Polished</p> ',
    18:'<p><strong>What is your appetite like?</strong></p> <p>1.Irregular, Scanty</p> <p>2.Strong, Unbearable</p> <p>3.Slow but steady</p> ',
    19:'<p><strong>What are some of your likable tastes?</strong></p> <p>1.Sweet / Sour / Salty</p> <p>2.Sweet / Bitter / Astringent</p> <p>3.Pungent / Bitter / Astringent</p>'
}

def get_ans(li):
    val = model.predict(li).item()
    praks ={
        0:'vata',
        1:'pitta',
        2:'kapha',
        3:'vata+pitta',
        4:'vata+kapha',
        5:'pitta+kapha'
    }
    return praks.get(val)


flag = False;
i = 0;
lis = []
limit = len(questions.items())
print(lis, limit)
def get_response(msg):
    global flag,i,limit,lis
    ans = ''
    if(flag):
        if i!=0:
            lis.append(int(msg)-1)
        ans = questions.get(i)
        if(i == limit):
            flag = False
            praki = get_ans([lis])
            ans = f'<p><strong>Your Prakriti is:</strong></p> {praki}'
            
        i = i + 1
        print(lis, limit,i,flag)
        return ans
    msg_list= []
    msg_list.append(msg)
    msg_count = vectorizer.transform(msg_list)
    tag = get_intent(msg_count)
    if tag == 'prakriti':
        flag = True
    for intent in intents["intent"]:
        if tag == intent["tag"]:
            ans = random.choice(intent["responses"])
            return (ans)


