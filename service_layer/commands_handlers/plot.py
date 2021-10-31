from domain.model import ChatMessage
from functools import lru_cache, partial

from datetime import timedelta, date, datetime
from typing import Dict, List, Tuple, Union
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
    user_messages: List[ChatMessage] = []

    with uow:
        ini_date, end_date = get_start_and_end_day()
        user_messages = uow.repo.get_all_messages_in_chat(chat_id=chat_id, initial_datetime=ini_date, end_datetime=end_date)
        uow.commit()
        
    user_ids = list({x.user_id for x in user_messages})

    my_list: List[Tuple[int, int]]=  []
    
    for user_id in user_ids:
        cant = len([x for x in user_messages if x.user_id ==  user_id])
        my_list.append((user_id, cant))
    my_list.sort(key=lambda tup: tup[1], reverse=True)

    user_ids = [tup[0] for tup in my_list]
    cant_mensajes = [tup[1] for tup in my_list]


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


# @lru_cache(maxsize=None)
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


def get_start_and_end_day(input_date: datetime) -> Tuple[datetime, datetime]:
    start = input_date
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(1)
    return start, end

def get_start_and_end_week(input_date: datetime) -> Tuple[datetime, datetime]:
    start = input_date - timedelta(days=input_date.weekday())
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=6)
    end += timedelta(1) # End of Sunday
    return start, end

def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - timedelta(days=next_month.day)

def get_start_and_end_month(input_date: datetime) -> Tuple[datetime, datetime]:
    start = input_date - timedelta(days=input_date.day) + timedelta(days=1)
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    # end = start + timedelta(days=6)
    end = last_day_of_month(start)
    end += timedelta(1) # End of last day of month
    return start, end

def get_start_and_end_alltime(input_date: datetime) -> Tuple[datetime, datetime]:
    return datetime.min, datetime.max

def group_chatmessages_by_hour(chat_messages: List[ChatMessage]) -> Tuple[List[int], List[List[ChatMessage]]]:
    hours = [x for x in range(24)]
    grouped_chat_messages_list: List[List[ChatMessage]] = [[] for _ in range(len(hours))]

    for chat_message in chat_messages:
        hour = chat_message.time.hour
        grouped_chat_messages_list[hour].append(chat_message)

    return hours, grouped_chat_messages_list

def group_chatmessages_by_weekday(chat_messages: List[ChatMessage]) -> Tuple[List[str], List[List[ChatMessage]]]:
    weekdays = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    grouped_chat_messages_list: List[List[ChatMessage]] = [[] for _ in range(len(weekdays))]

    for chat_message in chat_messages:
        weekday = chat_message.time.weekday()
        grouped_chat_messages_list[weekday].append(chat_message)

    return weekdays, grouped_chat_messages_list

def group_chatmessages_by_monthday(chat_messages: List[ChatMessage]) -> Tuple[List[int], List[List[ChatMessage]]]:
    max_day = max([x.time.day for x in chat_messages])

    monthdays = [x for x in range(1, max_day+1)]
    grouped_chat_messages_list: List[List[ChatMessage]] = [[] for _ in range(len(monthdays))]

    for chat_message in chat_messages:
        monthday = chat_message.time.day
        grouped_chat_messages_list[monthday].append(chat_message)

    return monthdays, grouped_chat_messages_list

def group_chatmessages_by_month(chat_messages: List[ChatMessage]) -> Tuple[List[int], List[List[ChatMessage]]]:
    months = [x for x in range(1, 13)]
    grouped_chat_messages_list: List[List[ChatMessage]] = [[] for _ in range(len(months))]

    for chat_message in chat_messages:
        monthday = chat_message.time.month - 1
        grouped_chat_messages_list[monthday].append(chat_message)

    return months, grouped_chat_messages_list

def group_chatmessages_by_user_id(chat_messages: List[ChatMessage], chat: Chat) -> Tuple[List[int], List[List[ChatMessage]]]:
    grouped_chat_messages_dict: Dict[int, List[ChatMessage]] = {}
    
    for user_id in set([x.user_id for x in chat_messages]):
        grouped_chat_messages_dict[user_id] = []        

    for chat_message in chat_messages:
        user_id = chat_message.user_id
        grouped_chat_messages_dict[user_id].append(chat_message)

    user_ids = list(grouped_chat_messages_dict.keys())
    grouped_chat_messages_list = list(grouped_chat_messages_dict.values())

    
    user_ids, grouped_chat_messages_list = list(zip(*sorted(zip(user_ids, grouped_chat_messages_list), reverse=True, key=lambda x: len(x[1]))))

    # Limit to 10
    user_ids = user_ids[:10]
    grouped_chat_messages_list = grouped_chat_messages_list[:10]

    nombres_usuarios = get_user_names(user_ids, chat)

    return nombres_usuarios, grouped_chat_messages_list

def group_chatmessages_by_date(chat_messages: List[ChatMessage]) -> Tuple[List[date], List[List[ChatMessage]]]:
    grouped_chat_messages_dict: Dict[date, List[ChatMessage]] = {}
    
    for the_date in set([x.time.date() for x in chat_messages]):
        grouped_chat_messages_dict[the_date] = []

    for chat_message in chat_messages:
        the_date = chat_message.time.date()
        grouped_chat_messages_dict[the_date].append(chat_message)

    dates = list(grouped_chat_messages_dict.keys())
    grouped_chat_messages_list = list(grouped_chat_messages_dict.values())

    return dates, grouped_chat_messages_list


def plot_horizontal_bars(data: List[ChatMessage], group_func, x_label: str, title: str, sort: bool = False) -> bytes:
    group_labels, grouped_chat_messages = group_func(data)
    totals = [len(group) for group in grouped_chat_messages]

    if sort:
        group_labels, totals =  list(zip(*sorted(zip(group_labels, totals), reverse=True, key=lambda x: x[1])))

    fig = plot_hor_bars(
        labels=group_labels,
        widths=totals,
        x_label=x_label,
        title=title,
    )

    return fig2bytes(fig)

def get_from_date_chat_messages(uow: AbstractUnitOfWork, chat_id: int, the_date: datetime = None) -> List[ChatMessage]:
    if the_date is None:
        the_date = datetime.today()
    with uow:
        ini_date, end_date = get_start_and_end_day(input_date=the_date)
        return uow.repo.get_all_messages_in_chat(chat_id, ini_date, end_date)

def get_chat_messages_between_dates(uow: AbstractUnitOfWork, chat_id: int, interval: str, the_date: datetime = None) -> List[ChatMessage]:
    if interval not in ["thisday", "thisweek", "thismonth", "alltime"]:
        interval = "thisday"

    if the_date is None:
        the_date = datetime.today()

    interval_getter_func = get_start_and_end_day

    if interval == "thisday":
        interval_getter_func = get_start_and_end_day
    elif interval == "thisweek":
        interval_getter_func = get_start_and_end_week
    elif interval == "thismonth":
        interval_getter_func = get_start_and_end_month
    else:
        interval_getter_func = get_start_and_end_alltime

    with uow:
        ini_date, end_date = interval_getter_func(input_date=the_date)
        return uow.repo.get_all_messages_in_chat(chat_id, ini_date, end_date)


def report_today_by_hour(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "thisday", datetime.today()), 
        group_func=group_chatmessages_by_hour, 
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por hora del día {date.today()}",
        )
    update.effective_message.reply_photo(image)
      
def report_thisweek_by_hour(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "thisweek", datetime.today()), 
        group_func=group_chatmessages_by_hour, 
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por hora de la semana ({date.today()})",
        )
    update.effective_message.reply_photo(image)    
    
def report_thisweek_by_weekday(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "thisweek", datetime.today()), 
        group_func=group_chatmessages_by_weekday, 
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por día de la semana ({date.today()})",
        )
    update.effective_message.reply_photo(image)    

def report_month_by_hour(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "thismonth", datetime.today()), 
        group_func=group_chatmessages_by_hour, 
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por hora del mes ({date.today()})",
        )
    update.effective_message.reply_photo(image)   

def report_month_by_weekday(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "thismonth", datetime.today()), 
        group_func=group_chatmessages_by_weekday, 
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por día de la semana del mes ({date.today()})",
        )
    update.effective_message.reply_photo(image)    
    
def report_month_by_date(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "thismonth", datetime.today()), 
        group_func=group_chatmessages_by_date, 
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por fecha del mes ({date.today()})",
        )
    update.effective_message.reply_photo(image)    
 
def report_alltime_by_hour(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "alltime", datetime.today()), 
        group_func=group_chatmessages_by_hour, 
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por hora de todo el tiempo",
        )
    update.effective_message.reply_photo(image)    
    
def report_alltime_by_weekday(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "alltime", datetime.today()), 
        group_func=group_chatmessages_by_weekday, 
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por día de la semana de todo el tiempo",
        )
    update.effective_message.reply_photo(image)    

def report_alltime_by_date(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "alltime", datetime.today()), 
        group_func=group_chatmessages_by_date, 
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por fecha de la semana de todo el tiempo",
        )
    update.effective_message.reply_photo(image)    
    
def report_alltime_by_month(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "alltime", datetime.today()), 
        group_func=group_chatmessages_by_month, 
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por mes de todo el tiempo",
        )
    update.effective_message.reply_photo(image)    




def report_today_by_users(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "thisday", datetime.today()), 
        group_func=partial(group_chatmessages_by_user_id, chat=update.effective_chat),
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por usuario del día {date.today()}",
        sort=True,
        )
    update.effective_message.reply_photo(image) 

def report_thisweek_by_users(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "thisweek", datetime.today()), 
        group_func=partial(group_chatmessages_by_user_id, chat=update.effective_chat),
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por usuario de la semana ({date.today()})",
        sort=True,
        )
    update.effective_message.reply_photo(image)    

def report_month_by_users(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "thismonth", datetime.today()), 
        group_func=partial(group_chatmessages_by_user_id, chat=update.effective_chat),
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por usuario del mes ({date.today()})",
        sort=True,
        )
    update.effective_message.reply_photo(image)   

def report_alltime_by_users(update: Update, context: CallbackContext, uow: AbstractUnitOfWork) -> None:
    chat_id = update.effective_chat.id
    image = plot_horizontal_bars(
        data=get_chat_messages_between_dates(uow, chat_id, "alltime", datetime.today()), 
        group_func=partial(group_chatmessages_by_user_id, chat=update.effective_chat),
        x_label="Cantidad de mensajes", 
        title=f"Total de mensajes por usuario de todo el tiempo",
        sort=True,
        )
    update.effective_message.reply_photo(image)    

 