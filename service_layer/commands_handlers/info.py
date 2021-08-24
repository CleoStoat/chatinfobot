import json 

from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def info_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:    
    mensaje_respuesta: str = json.dumps(json.loads(update.to_json()), indent=4, sort_keys=True)
    print(mensaje_respuesta)
    update.effective_message.reply_text(mensaje_respuesta)

    if update.effective_message is None:
        return

    if update.effective_message.text is None:
        return

    with uow:
        text = update.effective_message.text
        uow.repo.add_text_message(text)
        uow.commit()
    
    
