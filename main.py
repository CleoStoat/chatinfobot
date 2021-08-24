import datetime
import logging
from functools import partial

from telegram.ext import Updater
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.dispatcher import Dispatcher

import config
from adapters.orm import create_tables, start_mappers
from service_layer.commands_handlers.info import info_cmd
from service_layer.commands_handlers.infogroup import infogroup_cmd
from service_layer.msg_handler import msg_handler
from service_layer.unit_of_work import SqlAlchemyUnitOfWork


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

    # dispatcher.add_handler(CommandHandler("info", partial(info_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("mensajes", partial(infogroup_cmd, uow=uow)))
    dispatcher.add_handler(MessageHandler(Filters.all, partial(msg_handler, uow=uow)))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
