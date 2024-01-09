import pandas as pd
from joblib import load, dump
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("./bodyfind.csv")

X = df.drop('Dosha', axis ='columns')
y = df['Dosha']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2);

model = RandomForestClassifier()
model.fit(X_train,y_train)






