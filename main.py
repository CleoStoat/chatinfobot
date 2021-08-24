import datetime
import logging
from functools import partial
from typing import Any, Callable, List, Dict, Tuple, TypedDict, Union
from telegram.botcommand import BotCommand
from telegram.botcommandscope import BotCommandScope

from telegram.ext import Updater
from telegram.ext import dispatcher
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.dispatcher import Dispatcher

import config
from adapters.orm import create_tables, start_mappers
from service_layer.commands_handlers.info import info_cmd
from service_layer.commands_handlers.infogroup import infogroup_cmd
from service_layer.message_handlers.msg_handler import msg_handler
from service_layer.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork

class CommandData(TypedDict):
    callback: Callable
    name: str
    description: str

def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    start_mappers()
    create_tables()

    updater = Updater(token=config.get_bot_token())
    dispatcher: Dispatcher = updater.dispatcher

    # Instantiate SqlAlchemy Unit of Work
    uow = SqlAlchemyUnitOfWork()

    set_bot_commands(updater, uow)
    dispatcher.add_handler(MessageHandler(Filters.all, partial(msg_handler, uow=uow)))

    updater.start_polling()
    updater.idle()

def get_commands() -> List[CommandData]:
    commands = [
        CommandData(
            callback=infogroup_cmd,
            name="mensajes", 
            description="Muestra la cantidad de mensajes que se enviaron en este chat",
        ),
    ]

    return commands

def set_bot_commands(updater: Updater, uow: AbstractUnitOfWork) -> None:
    command_handlers: List[CommandHandler] = []
    bot_commands: List[Union[BotCommand, Tuple[str, str]]] = []

    for cmd in get_commands():
        command_handlers.append(
            CommandHandler(
                command=cmd["name"], 
                callback=partial(cmd["callback"], uow=uow),
            )
        )

        bot_commands.append(
            BotCommand(
                command=cmd["name"], 
                description=cmd["description"],
            )
        )

    dispatcher = updater.dispatcher
    for handler in command_handlers:
        dispatcher.add_handler(handler)

    # scope = BotCommandScope(type=BotCommandScope.ALL_CHAT_ADMINISTRATORS) 
    updater.bot.setMyCommands(commands=bot_commands)



if __name__ == "__main__":
    main()
