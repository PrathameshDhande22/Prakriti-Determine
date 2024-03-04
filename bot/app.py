from typing import TypedDict
from fastapi import FastAPI, WebSocketDisconnect, WebSocket
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware
from chatModule import chatWithUser
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Session
from logger import logger


class Base(DeclarativeBase):
    pass


class Reply(TypedDict):
    name: str
    message: str


class Chat(Base):
    __tablename__ = "chats"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    message = sqlalchemy.Column(sqlalchemy.String)
    detected_tag = sqlalchemy.Column(sqlalchemy.String)


app = FastAPI(debug=True, docs_url=None, redoc_url=None)
engine = sqlalchemy.create_engine("sqlite:///chats.db")
session = Session(engine)

Base.metadata.create_all(engine)
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
async def chatsocket(websocket: WebSocket):
    try:
        await websocket.accept()
        await websocket.send_json({"name": "bot", "message": "Welcome to AyurBot 🙏"})
        while True:
            received: Reply = await websocket.receive_json()
            chat = await chatWithUser(received, Chat, session)
            await websocket.send_json({"name": "bot", "message": chat["response"]})
    except WebSocketDisconnect as e:
        logger.info(f"Disconnected from {e.reason} and {e.code}")


if __name__ == "__main__":
    run("app:app", reload=True)
