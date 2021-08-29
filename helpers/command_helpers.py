from dataclasses import dataclass
from functools import partial
from typing import Callable, List, Tuple, Union

from telegram.botcommand import BotCommand
from telegram.ext import Updater
from telegram.ext.commandhandler import CommandHandler

from service_layer.unit_of_work import AbstractUnitOfWork


@dataclass
class CommandData:
    callback: Callable
    name: str
    description: str


def set_bot_commands(
    commands: List[CommandData], updater: Updater, uow: AbstractUnitOfWork
) -> None:
    command_handlers: List[CommandHandler] = []
    bot_commands: List[Union[BotCommand, Tuple[str, str]]] = []

    for cmd in commands:
        command_handlers.append(
            CommandHandler(
                command=cmd.name,
                callback=partial(cmd.callback, uow=uow),
            )
        )

        bot_commands.append(
            BotCommand(
                command=cmd.name,
                description=cmd.description,
            )
        )

    dispatcher = updater.dispatcher
    for handler in command_handlers:
        dispatcher.add_handler(handler)

    # scope = BotCommandScope(type=BotCommandScope.ALL_CHAT_ADMINISTRATORS)
    updater.bot.setMyCommands(commands=bot_commands)
