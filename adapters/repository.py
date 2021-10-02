from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple

import config
from domain.model import ChatMessage
from sqlalchemy.orm import Session, session
from sqlalchemy.sql import func


class AbstractRepository(ABC):
    @abstractmethod
    def add_message(self, user_id: int, chat_id: int, time: datetime) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_messages(self, chat_id: int) -> List[ChatMessage]:
        raise NotImplementedError

    @abstractmethod
    def get_list_of_users_msg_count(self) -> List[Tuple[int, int]]:
        raise NotImplementedError

    @abstractmethod
    def get_all_messages(self) -> List[ChatMessage]:
        raise NotImplementedError

    @abstractmethod
    def get_all_messages_in_chat(
        self,
        chat_id: int,
        initial_datetime: datetime = None,
        end_datetime: datetime = None,
    ) -> List[ChatMessage]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def add_message(self, user_id: int, chat_id: int, time: datetime) -> None:
        chat_msg = ChatMessage(user_id, chat_id, time)
        self.session.add(chat_msg)

    def get_messages(self, chat_id: int) -> List[ChatMessage]:
        result = self.session.query(ChatMessage).filter_by(chat_id=chat_id).all()
        self.session.expunge_all()
        return result

    def get_list_of_users_msg_count(self) -> List[Tuple[int, int]]:
        result = (
            self.session.query(
                ChatMessage.user_id,
                func.count(ChatMessage.time),
            )
            .group_by(ChatMessage.user_id)
            .all()
        )
        self.session.expunge_all()
        return

    def get_all_messages(self) -> List[ChatMessage]:
        chat_messages = self.session.query(ChatMessage).all()
        self.session.expunge_all()
        return chat_messages

    def get_all_messages_in_chat(
        self,
        chat_id: int,
        initial_datetime: datetime = None,
        end_datetime: datetime = None,
    ) -> List[ChatMessage]:
        if initial_datetime is None:
            initial_datetime = datetime.min
        if end_datetime is None:
            end_datetime = datetime.max

        chat_messages = (
            self.session.query(ChatMessage)
            .filter_by(chat_id=chat_id)
            .filter(
                ChatMessage.time >= initial_datetime,
                ChatMessage.time <= end_datetime,
            )
            .all()
        )
        self.session.expunge_all()
        return chat_messages
