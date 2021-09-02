from datetime import datetime
from dataclasses import dataclass


@dataclass()
class ChatMessage:
    user_id: int
    chat_id: int
    time: datetime


@dataclass()
class Chats:
    chat_id: int

@dataclass()
class Staff:
    user_id: int
