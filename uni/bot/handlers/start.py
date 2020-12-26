import logging
from bot.handlers.common import *
from bot.handlers.help import reply_short_help

from telegram import User, Bot

def start(update: Update, context: CallbackContext) -> None:
    logging.info("Received -> {} command to execute full text: {}".format(Commands.start, update.message.text))

    if is_user_registered(update.message.from_user):
        reply_welcome(update, context)
        reply_short_help(update, context)
    else:
        reply_welcome(update, context)
        reply_registration_required(update, context, update.message.from_user)

def get_command_handler() -> CommandHandler:
    return CommandHandler(Commands.start, start)