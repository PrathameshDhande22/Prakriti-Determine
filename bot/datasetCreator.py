import os
import pandas as pd
from sqlalchemy import Delete
from database import initDB, Prakriti
from question import questions


def addMoreDataFromDB():
    session = initDB()
    df = pd.read_csv(os.path.join("Dataset", "data.csv"))
    newdf = pd.read_sql_table("dataset", session.connection())
    newdf.drop(columns="id", inplace=True)
    newdf.columns = df.columns
    df1 = pd.concat([df, newdf], ignore_index=True)
    df1.to_csv(os.path.join("Dataset", "data.csv"), index=False)
    stmt = Delete(Prakriti)
    session.execute(stmt)


def createDataset():
    df = pd.read_csv(os.path.join("Dataset", "data.csv"))
    doshas = ["Vata", "Pitta", "Kapha",
              "vata+pitta", "vata+kapha", "pitta+kapha"]
    df["Dosha"] = df.iloc[:, -1].map(
        {0: doshas[0], 1: doshas[1], 2: doshas[2],
            3: doshas[3], 4: doshas[4], 5: doshas[5]}
    )
    for i in range(20):
        curr = questions.get(i).get("options")
        df[df.columns[i]] = df.iloc[:, i].map(curr)
    df.to_csv(os.path.join("Dataset", "prakriti.csv"), index=False)


choice = int(input(
    "Enter 1 To add the data from database to dataset\nEnter 2 to recreate the Prakrit Dataset\nEnter Your choice:"))
match choice:
    case 1: addMoreDataFromDB()
    case 2: createDataset()
    case _: print("Please Give Proper Input.")
