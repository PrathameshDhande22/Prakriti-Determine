import os
import pandas as pd
from logger import logger

df = pd.read_csv(os.path.join("Dataset", "diet.csv"))


def recommend_Diet(prakriti: str) -> list[str]:
    try:
        recommends = (
            df.loc[df["Doshas"] == prakriti]
            .drop("Doshas", axis=1)
            .to_numpy()
            .tolist()[0]
        )
        recommends[0] = f"<b>To Consume : </b>{recommends[0]}"
        recommends[1] = f"<b>To Avoid : </b>{recommends[1]}"
        return recommends
    except IndexError as ie:
        logger.error(f"Rather than Prakrit given {ie}")
