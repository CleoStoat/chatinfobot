import json
from typing import List 

from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def broadcast_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:    
    # Comprobar que es miembro del staff
    if update.effective_user.id not in config.get_staff_ids():
        return

    # Comprobar que es una respuesta a un mensaje
    if update.effective_message.reply_to_message is None:
        update.effective_message.reply_text("Usa el comando respondiendo a un mensaje")
        return


    with uow:
        # Obtener todos los chats donde está el bot
        all_chatmessages = uow.repo.get_all_messages()

        all_chat_ids: List[int] = list(set([x.chat_id for x in all_chatmessages]))

        for chat_id in all_chat_ids:
            try:
                context.bot.copy_message(                
                    chat_id=chat_id, 
                    from_chat_id=update.effective_chat.id,
                    message_id=update.effective_message.reply_to_message.message_id,
                )
            except Exception:
                pass
        uow.commit()

    
    
    
    
