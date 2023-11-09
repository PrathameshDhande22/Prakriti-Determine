from fastapi import FastAPI, status
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatModule import get_responses


# creating the model
class MessageModel(BaseModel):
    name: str
    message: str


app = FastAPI(debug=True)

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


@app.post("/chat", status_code=status.HTTP_200_OK)
def chats(message: MessageModel):
    reply = get_responses(message.message)
    print(f"Reply for message -> {message.message} => {reply}")
    return {"name": "Bot", "message": reply}


if __name__ == "__main__":
    run("app:app", reload=True)
