from typing import Any, NamedTuple, TypedDict


class Response(TypedDict):
    response: str | list
    tag: str


class ChatResponse(TypedDict):
    response: dict | str | list


class Reply(TypedDict):
    name: str
    message: Any


class PrakritBotResponse(NamedTuple):
    index: int
    prakriti: str
