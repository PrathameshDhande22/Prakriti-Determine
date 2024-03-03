from json import JSONDecodeError
from fastapi import FastAPI, WebSocketDisconnect, status, WebSocket
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatModule import getResponseChat, saveEveryResponse
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


# creating the model
class MessageModel(BaseModel):
    name: str
    message: str


class Chat(Base):
    __tablename__ = "chats"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    message = sqlalchemy.Column(sqlalchemy.String)
    detected_tag = sqlalchemy.Column(sqlalchemy.String)


app = FastAPI(debug=True)
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
        while True:
            received = await websocket.receive_json()
            chat = getResponseChat(received["message"])
            print(chat["tag"])
            saveEveryResponse(received, Chat, session, chat["tag"])
            await websocket.send_json({"name": "bot", "message": chat["response"]})
    except WebSocketDisconnect as e:
        print(e)


if __name__ == "__main__":
    run("app:app", reload=True)
