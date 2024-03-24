import time
from json import JSONDecodeError

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from chatModule import chatWithUser
from database import initDB
from logger import logger
from models import ChatResponse, Reply

app = FastAPI(debug=True, docs_url=None, redoc_url=None)
session = initDB()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"message": "hello World"}


@app.websocket("/chat", name="Chatbot")
async def chatsocket(websocket: WebSocket) -> Reply:
    try:
        await websocket.accept()
        await websocket.send_json({"name": "bot", "message": "Welcome to AyurBot 🙏"})
        while True:
            received: Reply = await websocket.receive_json()
            chat: ChatResponse = await chatWithUser(received, session)
            if isinstance(chat.get("response"), list):
                for resps in chat.get("response"):
                    await websocket.send_json({"name": "bot", "message": resps})
                    time.sleep(1.1)
            else:
                await websocket.send_json(
                    {"name": "bot", "message": chat.get("response")}
                )
    except WebSocketDisconnect as e:
        logger.error(f"Disconnected from {e.reason} and {e.code}")
    except JSONDecodeError as js:
        await websocket.close()
        logger.error(f"Error While recieving JSON Data => {js}")
    except AttributeError as ae:
        await websocket.close()
        logger.error(f"The Received message is in wrong format => {ae}")


if __name__ == "__main__":
    run("app:app", reload=True)
