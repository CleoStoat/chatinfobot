import json 

from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def plot_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:    

    with uow:
        uow.commit()
    
    
