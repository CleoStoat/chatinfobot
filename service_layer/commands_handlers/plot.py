import datetime
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from service_layer.unit_of_work import AbstractUnitOfWork
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext


def plot_cmd(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    plt.rcdefaults()
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)

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

    y_pos = np.arange(len(nombres_usuarios))

    ax.barh(y_pos, cant_mensajes, align="center")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(nombres_usuarios)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel("Mensajes")
    ax.set_title(f"Cantidad de mensajes de hoy ({datetime.date.today()})")

    # plt.show()

    buf = fig2bytes(fig)

    # img.show()

    update.effective_message.reply_photo(buf)


# def fig2img(fig):
#     """Convert a Matplotlib figure to a PIL Image and return it"""
#     import io

#     buf = io.BytesIO()
#     fig.savefig(buf)
#     buf.seek(0)
#     img = Image.open(buf)
#     return img


def fig2bytes(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io

    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return buf
