import json 

from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def infogroup_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:    

    with uow:
        mensajes = uow.repo.get_messages(update.effective_chat.id)
        text = str(len(mensajes))
        update.effective_message.reply_text(text)
        uow.commit()
    
    
