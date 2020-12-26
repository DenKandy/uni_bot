import logging
from bot.handlers.common import *

def reply_help(update: Update, context: CallbackContext, slot: int) -> None:
    logging.info("Received -> {} command to execute full text: {}".format(Commands.help, update.message.text))
    update.message.reply_text(
        'Для реалізація запитів використовуйте, будь ласка, наступні команди:\n')
    
    commands_str = ''
    for command, desc in commands_help.items():
        commands_str = '{}\n /{} {}'.format(commands_str, command, desc[slot])
    
    update.message.reply_text(commands_str)

def reply_detail_help(update: Update, context: CallbackContext) -> None:
    reply_help(update, context, 1)

def reply_short_help(update: Update, context: CallbackContext) -> None:
    reply_help(update, context, 0)

def get_command_handler() -> CommandHandler:
    return CommandHandler(Commands.help, reply_detail_help)