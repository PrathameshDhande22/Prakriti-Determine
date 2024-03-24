import requests
import os
from models import Intents
from dotenv import load_dotenv

load_dotenv(os.path.join(".env"))


def getIntents() -> Intents:
    url = f'https://api.jsonsilo.com/{os.environ.get("FILE_UUID")}'
    headers = {
        'X-SILO-KEY': os.environ.get("JSILO_API_KEY"),
        'Content-Type': 'application/json'
    }
    new_data = requests.get(url, headers=headers)
    return new_data.json()
