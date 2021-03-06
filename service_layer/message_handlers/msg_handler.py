from datetime import datetime, timezone
import json 

from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def msg_handler(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:    
    if update.effective_message is None:
        return

    if update.effective_message.text is None:
        return

    user_id: int = update.effective_user.id
    chat_id: int = update.effective_chat.id
    time: datetime = utc_to_local(update.effective_message.date)

    with uow:
        uow.repo.add_message(user_id, chat_id, time)
        uow.commit()
    
    
def utc_to_local(utc_dt) -> datetime:
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
