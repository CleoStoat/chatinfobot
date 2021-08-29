import datetime
from typing import List

from service_layer.unit_of_work import AbstractUnitOfWork
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from helpers.graph_helpers import fig2bytes
from service_layer.plotting import plot_hor_bars


def plot_cmd(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    nombres_usuarios: List[int] = []
    cant_mensajes: List[int] = []

    with uow:
        user_messages = uow.repo.get_list_of_users_msg_count()
        user_messages.sort(key=lambda x: x[1], reverse=True)
        for user, msg_count in user_messages:
            nombres_usuarios.append(user)
            cant_mensajes.append(msg_count)
        uow.commit()

    for i in range(300):
        nombres_usuarios.append(i)
        cant_mensajes.append(i)

    # Only show top 30 users
    amm = 30
    nombres_usuarios = nombres_usuarios[:amm]
    cant_mensajes = cant_mensajes[:amm]

    fig = plot_hor_bars(
        labels=nombres_usuarios,
        widths=cant_mensajes,
        x_label="Mensajes",
        title=f"Cantidad de mensajes de hoy ({datetime.date.today()})",
    )

    update.effective_message.reply_photo(fig2bytes(fig))
