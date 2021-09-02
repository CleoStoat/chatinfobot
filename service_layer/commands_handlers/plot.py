from functools import lru_cache
import datetime
from typing import Dict, List, Tuple
from telegram.chat import Chat

from telegram.chatmember import ChatMember
from telegram.error import TelegramError

from service_layer.unit_of_work import AbstractUnitOfWork
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
import telegram

from helpers.graph_helpers import fig2bytes
from service_layer.plotting import plot_hor_bars, plot_line


def plot_cmd(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    user_ids: List[int] = []
    cant_mensajes: List[int] = []

    chat_id = update.effective_chat.id

    with uow:
        user_messages = uow.repo.get_all_messages_in_chat(chat_id=chat_id)
        
        user_ids = list({x.user_id for x in user_messages})

        my_list: List[Tuple[int, int]]=  []
        
        for user_id in user_ids:
            cant = len([x for x in user_messages if x.user_id ==  user_id])
            my_list.append((user_id, cant))
        my_list.sort(key=lambda tup: tup[1], reverse=True)

        user_ids = [tup[0] for tup in my_list]
        cant_mensajes = [tup[1] for tup in my_list]

        uow.commit()

    chat = update.effective_chat
    nombres_usuarios: List[str] = []

    nombres_usuarios = get_user_names(user_ids, chat)

    fig = plot_hor_bars(
        labels=nombres_usuarios,
        widths=cant_mensajes,
        x_label="Mensajes",
        title=f"Cantidad de mensajes de hoy ({datetime.date.today()})",
    )

    update.effective_message.reply_photo(fig2bytes(fig))

def get_user_names(user_ids: List[int], chat: Chat) -> List[str]:
    user_names = []
    for user_id in user_ids:
        user_names.append(get_chat_member_name(user_id, chat))

    return user_names


@lru_cache(maxsize=None)
def get_chat_member_name(user_id: int, chat: Chat) -> str:
    try:
        member: ChatMember = chat.get_member(user_id=user_id)
        if member.user.username is None:
            return member.user.full_name
        else:
            return "@" + member.user.username
    except TelegramError:
        return "Unknown"


def plot_active_hours_cmd(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    hours: List[int] = []
    cant_mensajes: List[int] = []

    hours_msg_count: Dict[int, int] = {hour: 0 for hour in range(24)}

    with uow:
        chat_messages = uow.repo.get_all_messages()
        
        for chat_message in chat_messages:
            hour = chat_message.time.hour
            hours_msg_count[hour] += 1
        
        uow.commit()

    chat = update.effective_chat

    hours = list(hours_msg_count.keys())
    cant_mensajes = list(hours_msg_count.values())

    fig = plot_hor_bars(
        labels=hours,
        widths=cant_mensajes,
        x_label="Mensajes",
        title="Cantidad de mensajes por hora",
    )

    update.effective_message.reply_photo(fig2bytes(fig))

def plot_active_weekdays_cmd(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    weekdays: List[int] = []
    cant_mensajes: List[int] = []

    wd_code = {
        0: "Lunes",
        1: "Martes",
        2: "Miercoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sabado",
        6: "Domingo",
    }
    weekday_msg_count: Dict[int, int] = {wd_code[weekday_num]: 0 for weekday_num in range(7)}

    with uow:
        chat_messages = uow.repo.get_all_messages()
        
        for chat_message in chat_messages:
            weekday = wd_code[chat_message.time.weekday()]
            weekday_msg_count[weekday] += 1
        
        uow.commit()

    weekdays = list(weekday_msg_count.keys())
    cant_mensajes = list(weekday_msg_count.values())

    fig = plot_hor_bars(
        labels=weekdays,
        widths=cant_mensajes,
        x_label="Mensajes",
        title="Cantidad de mensajes por día de la semana",
    )

    update.effective_message.reply_photo(fig2bytes(fig))


    
def plot_month_cmd(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    days: List[int] = []
    cant_mensajes: List[int] = []

    day_msg_count: Dict[int, int] = {day: 0 for day in range(32)}

    with uow:
        chat_messages = uow.repo.get_all_messages()
        
        for chat_message in chat_messages:
            day = chat_message.time.day
            day_msg_count[day] += 1
        
        uow.commit()

    days = list(day_msg_count.keys())
    cant_mensajes = list(day_msg_count.values())

    fig = plot_line(
        x_labels=days,
        heights=cant_mensajes,
        x_label="Dias",
        y_label="Mensajes",
        title="Cantidad de mensajes por dia del mes",
    )

    update.effective_message.reply_photo(fig2bytes(fig))