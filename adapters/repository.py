from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

import config
from domain.model import ChatMessage
from sqlalchemy.orm import Session, session


class AbstractRepository(ABC):

    @abstractmethod
    def add_message(self, user_id: int, chat_id: int, time: datetime) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_messages(self, chat_id: int) -> List[ChatMessage]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def add_message(self, user_id: int, chat_id: int, time: datetime) -> None:
        chat_msg = ChatMessage(user_id, chat_id, time)
        self.session.add(chat_msg)
        
    def get_messages(self, chat_id: int) -> List[ChatMessage]:
        return self.session.query(ChatMessage).filter_by(chat_id = chat_id).all()
        