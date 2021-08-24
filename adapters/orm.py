from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import mapper, relationship

from domain.model import ChatMessage
import config

metadata = MetaData()

chat_message = Table(
    "chat_messages",
    metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=False),
    Column("chat_id", Integer, primary_key=True, autoincrement=False),
    Column("time", DateTime, primary_key=True, autoincrement=False),
)

def start_mappers():
    mapper(ChatMessage, chat_message)


def create_tables():
    engine = create_engine(config.get_sqlite_uri())
    metadata.create_all(engine)
